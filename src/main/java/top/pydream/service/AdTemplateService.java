package top.pydream.service;

import top.pydream.domain.AdTemplate;

import java.util.List;

public interface AdTemplateService {

    AdTemplate findById(Long id);

    List<AdTemplate> findRelatedAds(String wechat);
}
