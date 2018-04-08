package top.pydream.generator.service;

import top.pydream.generator.domain.News;

import java.util.List;

public interface NewsService {
    List<News> findByTag(String tag);
    List<News> findBySecondLike(String second);
}
