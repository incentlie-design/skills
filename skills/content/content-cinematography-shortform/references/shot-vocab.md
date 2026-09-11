# 封闭镜头词表

禁止用「电影感」「高级感」当参数。生成提示里的焦段不是实测镜头。

## 景别 `size`

`ELS` `LS` `FS` `MS` `MCU` `CU` `ECU`

功能：远景地理/关系；中景行动；近景反应；特写物件线索。不要为凑清单每种都拍。

## 角度 `angle`

`eye` `high` `low` `overhead` `ground`

俯/仰改变权力，不改变已锁站位。

## 运动 `move`

`static` `push` `pull` `pan` `tilt` `track` `handheld`

默认 `static`。运动必须有事件或注意力动机、起止、跟随对象、停止点。

## 轴线

每 `scene_id` 一条 `axis` 与 `axis_side`。越轴要有观众可见过渡。生成图是独立样本，不写轴线就会左右对调。
