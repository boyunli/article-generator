package top.pydream.dao;

import org.springframework.stereotype.Service;
import top.pydream.domain.AdTemplate;

@Service
public interface AdTemplateMapper {

    AdTemplate selectById(Long id);

    Integer selectMaxId();
}
