# 第06段重测说明

根据用户上传的 `MiniMaxH3_Director_00004_.mp4`（8秒、24fps、864×480）修订。视频内嵌 timeline_data 显示 commonEnabled=true，而 segment.prompt 又包含公共 subject_definitions；这是重复配置。附件编号1–5是对应的。

## 正确粘贴

1. 保持 r2v 和 Shared Params 开启。
2. Shared 文本框只放 `common-prompt.txt`。
3. 清空第06 Group 原来的文本，粘贴 `groups/06-launch-block-bridge.txt` 全文。本文件以 Picture 5 的定义开头，没有 subject_definitions 标题。
4. Shared Picture 1–4 保持分配表配置。本段 Picture 5 换成 `references/states/aegis-airborne-shield.png`，移除原 C-blade-contact。
5. 不要把 `../prompts/06-launch-block-bridge.txt` 放到启用 Shared 的 Group；它是 Shared 关闭时使用的完整版本。

本次只调整提示词与本段参考图。保留测试文件中记录的4 steps、CFG 1、simple scheduler、Turbo LoRA强度1以及相同种子（如可用），便于比较。此建议不是对这些采样参数的独立验证。

## 动作变化

- 本次第06段全程盾形态，减少一次刀盾转换，消除胸甲斩击参考带来的冲突。大刀仍保留在第07段。
- 0–2秒：全身同框建立尺度，短促蓄力，向画面右上方爆发起飞。
- 2–4.5秒：爪盾接触后肘部压回、腰部扭转、整个人被击偏数个身位；同镜头显示接触与位移。
- 4.5–8秒：制动脱险，巨掌落在桥面，桥梁从接触处断裂；结尾仍举盾，胸甲未受刀伤。

## 检查通过条件

- 开场全身同框具有约16:1高度关系，切镜后不把Aegis放大成巨人。
- 爪盾先接触，随后出现光效和身体位移；没有持续静止顶推。
- 同一侧向全景内看清手掌击桥、桥面弯折、中央桥段下落。
- 末尾仍是盾、无斩击、无胸部碎裂；第07段再开始进攻。

尚未重新渲染。新图盾缘较厚，提示词只保留能量投影与连接关系；比例参考仍有误差，文字无法保证纠正。如果8秒内仍丢失击桥因果，下一轮把起飞挡爪与断桥脱险拆成两个独立源片段，再剪回原时长。
