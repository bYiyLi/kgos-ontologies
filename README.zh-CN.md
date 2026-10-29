# KG OS Ontologies

**KG OS 官方公开本体模型库：可复用、可验证、可按版本引用的 Property Graph 模型。**

此仓库提供供 AI 和人类参考的领域 Ontology，而不是 KG OS 内置领域模型。**安装 KG OS、安装 Skill 或阅读本仓库都不会自动创建 Definition、导入 Knowledge 或改变 Branch。**

[English](README.md)

## 当前模型

| 模型 | 用途 | 唯一定义来源 | 查询与测试 |
| --- | --- | --- | --- |
| [VLog 事件本体](models/vlog/README.md) | 事件、参与对象、分类、时间、地点、来源、验证和后续关系 | [Ontology](models/vlog/ontology.md) | [Cypher](models/vlog/cypher.md) · [合成测试资料](models/vlog/tests/) |
| [AIMemory 长期记忆本体](models/ai-memory/README.md) | 记忆类型、主题、召回线索、来源、经历及演进 | [Ontology](models/ai-memory/ontology.md) | [Cypher](models/ai-memory/cypher.md) · [合成测试](models/ai-memory/tests/) · [专属 Skill](models/ai-memory/skills/kgos-memory-standards/SKILL.md) |

当前提供两套可选模型，不把教学案例、所有领域词语或 KG OS Kernel 内部结构冒充通用本体。AIMemory 的主题与类型在 Knowledge 层组织，Domain 不隔离记忆实例或权限。

## AI 如何复用

1. 阅读模型说明，按固定的 Git Tag 或 Commit 获取 `ontology.md`、`cypher.md`，避免使用会漂移的 `main` 作为长期证据。
2. 先读取目标 KG OS 的 Instance、Branch、固定 State、已有 Ontology、Knowledge 和关系，确定要回答的实际业务问题。
3. **优先复用已有结构**。确有语义缺口才选择性适配必要的 Node、Relationship、Property、Constraint、Index 和 Domain。Domain 只组织 Definition，不是 Knowledge 的隔离层。
4. 在修改 Ontology、迁移 Knowledge、新建 Branch 前，先给出模型和数据影响方案并取得相应授权。
5. 按目标实例提供的 `kgos_docs` 合同执行修改，随后回读新 State，并运行必要的真实图查询。每个 YAML 代码块是一份 Definition，不是可整体执行的 Patch。

模型只是有条件的参考，不自动证明事件真实性、关系因果、跨版本连接或证据可信度。

## 唯一真源与版本

每套模型的 `models/<name>/ontology.md` 是**公开模型的唯一可维护定义真源**。如提供领域专属 `skills/<skill-name>/SKILL.md`，其行为规范也只在领域包维护一份。查询与测试随模型版本发布；KG OS Plugin 只能携带从指定 Git Commit **生成的模型和 Skill 固定快照**，不能在两处手工维护不同版本。

## 验证

```sh
python3 -m pip install -r requirements-test.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

这项检查负责 YAML、模型关系与查询测试资料的**静态一致性**，不是运行 KG OS 的真实数据库测试。首个 VLog 模型来自已做 KG OS/Lithograph 隔离测试的资源，未来修改必须重新取得实际运行验证，不能只用 CI 静态通过声称兼容。

仓库使用 [AGPL-3.0-only](LICENSE)。贡献范围见 [CONTRIBUTING.md](CONTRIBUTING.md)，KG OS 产品分发见 [kg-releases](https://github.com/bYiyLi/kg-releases)。
