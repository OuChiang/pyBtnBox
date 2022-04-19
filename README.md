## 介紹
pyBtnBox是一個可以快速創建按鈕櫃的小工具

<img src="https://user-images.githubusercontent.com/69313227/163719597-14eb7a6e-9fe0-4833-bd10-bc3a5241e449.png" width="300">

## 如何安裝

下載好pyBtnBox後，可從Edit>Preference>Add-ons做安裝
<img src="https://user-images.githubusercontent.com/69313227/163718432-2443da81-f5bd-4d50-ab3e-0f8492c5531f.png" width="600">



## 如何新增按鈕
1. 將寫好的python script放入相應的Menu資料夾內
( 可用面板上的PyFolder快速開啟Menu的資料夾 )

<img src="https://user-images.githubusercontent.com/69313227/163719635-58fd4e90-c230-4e2f-ab2b-2ce4ce570a6f.png" width="300">

2. 重新載入指令搞
( 面板上有Reload Scrupts的按鈕  )
<img src="https://user-images.githubusercontent.com/69313227/163720036-7519066d-7128-4093-8029-791515601ca1.png" width="300"> 


3. 完成
<img src="https://user-images.githubusercontent.com/69313227/163720125-d2cb3ef3-a042-46c3-9be7-bf3bdba1eb1a.png" width="300"> 


## 修改Text及Icon
- Text可從Layout做開啟
<img src="https://user-images.githubusercontent.com/69313227/163722094-dc3a56c1-983b-457f-ab73-05a2b5177bdc.png" width="300"> 

1. 開啟該Menu資料夾內，名為_menuData.json的檔案
(也可用面板上的MenuData按鈕做開啟)

<img src="https://user-images.githubusercontent.com/69313227/163721763-d1400982-3f39-4571-8edf-2d51c202c507.png" width="400"> 
<img src="https://user-images.githubusercontent.com/69313227/163721157-e12f4312-0424-437c-b6ad-04994f265cda.png" width="300"> 

2. 修改其text及icon即可(icon名稱可用Icon Viewer尋查)

<img src="https://user-images.githubusercontent.com/69313227/163721338-2ad60745-d3b8-4724-a802-206f1878a9d6.png" width="300"> 


## 新增Menu
1. 在pyFolders內新增資料夾(資料夾名稱即Menu名稱)
(pyFolders就是各Menu資料夾的上一層)
<img src="https://user-images.githubusercontent.com/69313227/163721866-71e38fc9-187c-4d46-86dc-02cb4d3edbba.png" width="400"> 

2. 重新載入指令搞
( 面板上有Reload Scrupts的按鈕  )
<img src="https://user-images.githubusercontent.com/69313227/163720036-7519066d-7128-4093-8029-791515601ca1.png" width="300"> 

3. 可從Menu選單做選擇
<img src="https://user-images.githubusercontent.com/69313227/163721918-ee937720-af55-4994-80df-ad90e6148f88.png" width="300"> 


## Layout
- Text可用於標註

<img src="https://user-images.githubusercontent.com/69313227/163722094-dc3a56c1-983b-457f-ab73-05a2b5177bdc.png" width="300"> 

- Input按鈕可將該python script導入text edior

<img src="https://user-images.githubusercontent.com/69313227/163722465-af9104b2-0b86-41b2-b992-9fd4a02ca0f1.png" width="300"> 
<img src="https://user-images.githubusercontent.com/69313227/163722602-2ad84672-1f4b-4309-97ee-01a7531ff6c5.png" width="500"> 

- Order按鈕可調整按鈕上下順序(調整完需按SaveSetting按鈕保存)
<img src="https://user-images.githubusercontent.com/69313227/163722687-173d6d6d-51a8-4712-a7ef-a89f625c4215.png" width="300"> 
<img src="https://user-images.githubusercontent.com/69313227/163722818-7954bf5c-56bf-49b1-b2bc-8660e5deeca5.png" width="300"> 

## 已知問題
在Blender2.93及3.0，使用ImportHelper會無法回傳值而產生錯誤

似乎是因為提升至python3.9所產生的錯誤

到Blender3.1時已無出現此問題

## 作者
[Ou-HisnChiang](https://github.com/OuChiang)
