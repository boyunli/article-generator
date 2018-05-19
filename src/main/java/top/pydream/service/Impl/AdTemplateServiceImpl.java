package top.pydream.service.Impl;

import org.springframework.stereotype.Service;
import top.pydream.dao.AdTemplateMapper;
import top.pydream.domain.AdTemplate;
import top.pydream.service.AdTemplateService;

import javax.annotation.Resource;
import java.util.List;

@Service
public class AdTemplateServiceImpl implements AdTemplateService{

    @Resource
    AdTemplateMapper adTemplateMapper;

    @Override
    public AdTemplate findById(Long id) {
        return adTemplateMapper.selectById(id);
    }

    @Override
    public List<AdTemplate> findAdByCategoryAndWechat(String category, String wechat) {
        return adTemplateMapper.selectAdByCategoryAndWechat(category, wechat);
    }


}
