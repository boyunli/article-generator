package top.pydream.service;

import top.pydream.domain.News;

import java.util.List;

public interface NewsService {

    List<News> findByTag(String tag);

    List<News> findBySecondLike(String second);
}
