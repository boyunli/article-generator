package top.pydream.service.Impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import top.pydream.domain.News;
import top.pydream.repository.NewsRepository;
import top.pydream.service.NewsService;

import java.util.List;

@Service("NewsServiceImpl")
public class NewsServiceImpl implements NewsService {

    @Autowired
    private NewsRepository newsRepository;

    @Override
    public List<News> findByTag(String tag) {
        return newsRepository.findByTag(tag);
    }

    @Override
    public List<News> findBySecondLike(String second) {
        return newsRepository.findBySecondLike(second);
    }

}
