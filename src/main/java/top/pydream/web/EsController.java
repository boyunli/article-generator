package top.pydream.web;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.*;
import top.pydream.domain.*;
import top.pydream.service.AccountService;
import top.pydream.service.AdTemplateService;
import top.pydream.service.Impl.NewsServiceImpl;
import top.pydream.service.NewsService;
import top.pydream.utils.Common;
import top.pydream.utils.Synonyms;

import javax.validation.Valid;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@RestController
public class EsController {
    private static final Logger LOGGER = LoggerFactory.getLogger(EsController.class);

    private static String DELIMITER = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

    @Autowired
    private NewsService newsService;

    @Autowired
    private AccountService accountService;

    @Autowired
    private AdTemplateService adTemplateService;

    @PostMapping("/search")
    public ResponseEntity<?> createPseudo(@Valid @RequestBody SearchForm searchForm, Errors errors) {

        AjaxResponseBody result = new AjaxResponseBody();

        if (errors.hasErrors()) {
            result.setMsg(errors.getAllErrors()
                    .stream().map(x -> x.getDefaultMessage())
                    .collect(Collectors.joining(",")));
            return ResponseEntity.badRequest().body(result);
        }

        // 获取微信模板
        String wechat = searchForm.getWechat();
        String category = searchForm.getCategory();
        Account account = accountService.findByCategoryAndWeixin(category, wechat);
        List<AdTemplate> ads = adTemplateService.findAdByCategoryAndWechat(category, wechat);
        List<Long> ids = new ArrayList<>();
        ads.forEach(ad -> ids.add(ad.getId()));

        // 获取伪原创 文章
        String keyword = searchForm.getKeyword();
        List<News> news = newsService.searchContent(0,100, keyword, category);
        int newsNum = news.size();
        LOGGER.info("\n searchNews: 匹配到news数量： [" + newsNum + "] \n ");
        List<String> paragraphs = Common.divideParas(news);

        // 结尾
        String end = "";
        if (category.contains("包"))
            end = "全部内容，一起交流更多包包知识，欢迎添加玲珑皮具微信，感谢阅读！";
        else if (category.contains("表"))
            end = "全部内容，一起交流更多腕表知识，欢迎添加微信: 【" + wechat + "】。感谢阅读！";

        List<PseudoNews> pseudoNews = new ArrayList<>();
        for (int i=0; i<=3; i++){
            int[] indexParams = Common.randomPara(1, paragraphs.size()-1, 4);
            String second = "";
            String third = "";
            second += paragraphs.get(indexParams[0]) + paragraphs.get(indexParams[1]);
            third += paragraphs.get(indexParams[2]) + paragraphs.get(indexParams[3]);

            int index = (int) Math.round(Math.random()*(ids.size()-1));
            if (index > ids.size()){
                index = ids.size() - 1;
            }
            long random = ids.get(index);
            AdTemplate template = adTemplateService.findById(random);
            String union = DELIMITER + keyword + "。" + account.getDesc() + "<br/><br/>"
                    + DELIMITER + template.getTemplate() + "<br/><br/>"
                    + DELIMITER + Synonyms.synonymsReplacement(second, 0.6) + keyword + "。<br/><br/>"
                    + DELIMITER + Synonyms.synonymsReplacement(third, 0.6)  + "<br/><br/>"
                    + DELIMITER + "以上就是" + keyword + end;
            int newsIndex = (int) Math.round(Math.random()*(newsNum-1));
            News randomNews = news.get(newsIndex);
            pseudoNews.add(new PseudoNews(randomNews.getTitle(), randomNews.getTag(), union));
        }

        if (pseudoNews.isEmpty()) {
            result.setMsg("没有符合 " + keyword + " 的伪原创， 请换一个关键词试试!");
        } else {
            result.setMsg("success");
        }
        result.setResult(pseudoNews);
        return ResponseEntity.ok(result);
    }
}
