package top.pydream.dao;

import org.springframework.stereotype.Repository;
import top.pydream.domain.Account;

@Repository
public interface AccountMapper {

    Account selectByWechat(String wechat);
}
