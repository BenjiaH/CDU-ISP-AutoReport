# Change Log

All notable changes to this project will be documented in this file.

---

## [1.2.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.2.0.release)

### (2022-1-3)

- **Incompatible changed:configuration segments format([`wechat_type`, `api`, `sendkey`, `userid`](../../commit/bcd6e8304fef833eef22d4940259baa1acec61c9#diff-00064dc5d2c5e2552c4d60b93722af776e9efca92fda5d9c9c06f33ce355f58b))**
- Added:go-scf push channel
- Added:sct.ftqq push channel
- Added:retry to push WeChat message and email
- Removed:sc.ftqq push channel
- Fixed:bugs

---

## [1.1.2.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.2.release)

### (2021-7-25)

- Added:error message prompt
- Changed:enable SSL in SMTP
- Fixed:parse the latest record correctly
- Fixed:bugs

---

## [1.1.1.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.1.release)

### (2021-6-14)

- Fixed:reset the error flag correctly
- Optimized:other details

---

## [1.1.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.1.0.release)

### (2021-4-2)

- **Incompatible changed:configuration segments format([time](../../commit/8f859965bbb635a19ef750daa857c8c7e081dd3e) & [switch](../../commit/1a9f69d8efd757b897bfcacc1249e809bc9b9219))**
- Added:fake_useragent to get random user-agents
- Added:BeautifulSoup4 to match information more stably
- Added:loguru for better logging
- Added:modify Email style by template html file
- Added:debug mode
- Optimized:report process
- Changed:WeChat push style
- Fixed:bugs

---

## [1.0.1.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.0.1.release)

### (2021-2-27)

- Fixed:bugs

---

## [1.0.0.release](https://github.com/BenjiaH/CDU-ISP-AutoReport/releases/tag/1.0.0.release)

### (2021-2-18)

- Added: Report automatically
- Added: Push notifications in dual channels(Email, Wechat)
- Added: Multiple accounts mode
- Added: Security
- Added: Hosts status checks

---

```N/A
   _____ _____  _    _      _____  _____ _____                    _        _____                       _   
  / ____|  __ \| |  | |    |_   _|/ ____|  __ \        /\        | |      |  __ \                     | |  
 | |    | |  | | |  | |______| | | (___ | |__) ______ /  \  _   _| |_ ___ | |__) |___ _ __   ___  _ __| |_ 
 | |    | |  | | |  | |______| |  \___ \|  ___|______/ /\ \| | | | __/ _ \|  _  // _ | '_ \ / _ \| '__| __|
 | |____| |__| | |__| |     _| |_ ____) | |         / ____ | |_| | || (_) | | \ |  __| |_) | (_) | |  | |_ 
  \_____|_____/ \____/     |_____|_____/|_|        /_/    \_\__,_|\__\___/|_|  \_\___| .__/ \___/|_|   \__|
                                                                                     | |                   
                                                                                     |_|                   
```