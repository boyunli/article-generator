package top.pydream.service.Impl;

import org.elasticsearch.action.admin.indices.analyze.AnalyzeAction;
import org.elasticsearch.action.admin.indices.analyze.AnalyzeRequestBuilder;
import org.elasticsearch.action.admin.indices.analyze.AnalyzeResponse;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.index.query.functionscore.FunctionScoreQueryBuilder;
import org.elasticsearch.index.query.functionscore.ScoreFunctionBuilders;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.core.ElasticsearchTemplate;
import org.springframework.data.elasticsearch.core.query.NativeSearchQueryBuilder;
import org.springframework.data.elasticsearch.core.query.SearchQuery;
import org.springframework.stereotype.Service;
import top.pydream.domain.News;
import top.pydream.repository.NewsRepository;
import top.pydream.service.NewsService;
import top.pydream.utils.SearchConstant;

import java.util.ArrayList;
import java.util.List;

@Service("NewsServiceImpl")
public class NewsServiceImpl implements NewsService {

    private static final Logger LOGGER = LoggerFactory.getLogger(NewsServiceImpl.class);

    Integer PAGE_SIZE = 12;
    Integer DEFAULT_PAGE_NUMBER = 0;

    /* 搜索模式 */
    String SCORE_MODE_SUM = "sum";
    Float MIN_SCORE = 10.0F;

    @Autowired
    private NewsRepository newsRepository;

    @Autowired
    private ElasticsearchTemplate elasticsearchTemplate;

    @Override
    public List<News> searchContent(Integer pageNumber, Integer pageSize,
                                   String keyword, String category) {
        if (pageSize == null || pageSize <= 0) {
            pageSize = PAGE_SIZE;
        }
        if (pageNumber == null || pageNumber < DEFAULT_PAGE_NUMBER) {
            pageSize = DEFAULT_PAGE_NUMBER;
        }
        LOGGER.info("\n searchNews: searchContent [" + keyword + "] \n ");

        List<String> searchTerms = getIkAnalyzeSearchTerms(keyword);
        LOGGER.info("\n searchNews: get IK analyzer terms: " + searchTerms + " \n ");
        SearchQuery searchQuery = getNewsSearchQuery(pageNumber, pageSize, category, searchTerms);
        Page<News> newsPage = newsRepository.search(searchQuery);
        return newsPage.getContent();
    }

    /**
     * 先根据 category 过滤news，再 进行短语查询 match parse
     * @param pageNumber  第几页
     * @param pageSize    每页数量
     * @param category    类型
     * @param searchTermList 分词后的短语
     * @return
     */
    private SearchQuery getNewsSearchQuery(Integer pageNumber, Integer pageSize,
                                           String category, List<String> searchTermList) {

        FunctionScoreQueryBuilder builder = QueryBuilders.functionScoreQuery();
        for (String searchTerm: searchTermList) {
            builder.add(QueryBuilders.matchPhraseQuery("title", searchTerm),
                    ScoreFunctionBuilders.weightFactorFunction(1000))
                    .add(QueryBuilders.matchPhraseQuery("content", searchTerm),
                            ScoreFunctionBuilders.weightFactorFunction(500))
                    .scoreMode(SCORE_MODE_SUM).setMinScore(MIN_SCORE);
        }
        Pageable pageable = new PageRequest(pageNumber, pageSize);
        return new NativeSearchQueryBuilder()
                .withPageable(pageable)
                .withFilter(QueryBuilders.termQuery("category", category))
                .withQuery(builder)
                .build();

    }

    /**
     * 调用 ES 获取 IK分词后结果
     * @param keyword news 内容
     * @return
     */
    private List<String> getIkAnalyzeSearchTerms(String keyword) {
        AnalyzeRequestBuilder ikRequest = new AnalyzeRequestBuilder(
                elasticsearchTemplate.getClient(),
                AnalyzeAction.INSTANCE,
                "price_system",
                keyword);
        ikRequest.setTokenizer("ik");
        ikRequest.setAnalyzer("ik_smart");
        List<AnalyzeResponse.AnalyzeToken> ikTokenList = ikRequest.execute().actionGet().getTokens();

        List<String> searchTermList = new ArrayList<>();
        ikTokenList.forEach(
                ikToken -> {
                    searchTermList.add(ikToken.getTerm());
                });
        return handlingIkResultTerms(searchTermList);
    }

    /**
     * 如果分词结果：洗发水（洗发、发水、洗、发、水）
     * - 均为词，保留
     * - 词 + 字，只保留词
     * - 均为字，保留字
     */
    private List<String> handlingIkResultTerms(List<String> searchTermList) {
        Boolean isPhrase = false;
        Boolean isWord = false;
        for (String term : searchTermList) {
            if (term.length() > SearchConstant.SEARCH_TERM_LENGTH) {
                isPhrase = true;
            } else {
                isWord = true;
            }
        }

        if (isWord & isPhrase) {
            List<String> phraseList = new ArrayList<>();
            searchTermList.forEach(term -> {
                if (term.length() > SearchConstant.SEARCH_TERM_LENGTH) {
                    phraseList.add(term);
                }
            });
            return phraseList;
        }

        return searchTermList;
    }
}
