package top.pydream.repository;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Component;
import top.pydream.domain.News;

import java.util.List;

@Component("NewsRepository")
public interface NewsRepository extends ElasticsearchRepository<News, String> {
}
