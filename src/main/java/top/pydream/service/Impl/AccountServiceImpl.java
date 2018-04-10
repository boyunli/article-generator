package top.pydream.service.Impl;

import org.springframework.stereotype.Service;
import top.pydream.dao.AccountMapper;
import top.pydream.domain.Account;
import top.pydream.service.AccountService;

import javax.annotation.Resource;

@Service
public class AccountServiceImpl implements AccountService {

    @Resource
    private AccountMapper accountMapper;

    @Override
    public Account findByWeixin(String wechat) {
        Account account =accountMapper.selectByWechat(wechat);
        return account;
    }
}
