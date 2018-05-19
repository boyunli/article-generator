package top.pydream.service;

import top.pydream.domain.Account;

public interface AccountService {
    Account findByCategoryAndWeixin(String category, String weixin);
}
