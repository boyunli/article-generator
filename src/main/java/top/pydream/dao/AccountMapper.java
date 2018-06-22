package top.pydream.dao;

import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;
import top.pydream.domain.Account;

@Repository
public interface AccountMapper {

    Account selectByCategoryAndWeixin(@Param("category") String category,
                                      @Param("wechat") String wechat);
}
