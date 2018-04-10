package top.pydream.service;

import top.pydream.domain.Account;

public interface AccountService {
    Account findByWeixin(String weixin);
}
