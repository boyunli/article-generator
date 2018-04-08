package top.pydream.generator.repository;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Component;
import top.pydream.generator.domain.News;

import java.util.List;

@Component("NewsRepository")
public interface NewsRepository extends ElasticsearchRepository<News, String> {

    /**
     * AND Query
     * @param tag
     * @return
     */
    public List<News> findByTag(String tag);

    /**
     * Like Query
     * @param second
     * @return
     */
    List<News> findBySecondLike(String second);
}
