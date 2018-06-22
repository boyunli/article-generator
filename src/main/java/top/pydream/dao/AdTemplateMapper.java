package top.pydream.dao;

import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Service;
import top.pydream.domain.AdTemplate;

import java.util.List;

@Service
public interface AdTemplateMapper {

    AdTemplate selectById(Long id);

    List<AdTemplate> selectAdByCategoryAndWechat(@Param("category") String category,
                                                 @Param("wechat") String wechat);
}
