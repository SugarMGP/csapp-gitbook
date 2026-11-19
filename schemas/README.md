# GitBook 配置 schema

`gitbook-docs.schema.yaml` 是 2026-11-19 从 [GitBook 官方 schema](https://api.gitbook.com/gitbook-docs.yaml) 下载的原文快照，供配置测试离线验证。不要手工编辑该快照；需要更新时从同一官方地址重新下载。

站点配置还需满足官方说明中的语义约束，例如默认空间唯一、空间 key 稳定以及目录映射有效；对应回归检查位于 `scripts/test_gitbook.py`。
