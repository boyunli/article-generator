package top.pydream.dao;

import org.springframework.stereotype.Service;
import top.pydream.domain.AdTemplate;

import java.util.List;

@Service
public interface AdTemplateMapper {

    AdTemplate selectById(Long id);

    List<AdTemplate> selectRelatedAds(String wechat);
}
