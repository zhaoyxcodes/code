var order = ['red', 'yellow', 'blue', 'green', 'red']
Page({
  data: {
    hidden:true,
    src:'',
    imglist:[]
  },
  onLoad(){
  },
  startTakePhoto() {
    const ctx = wx.createCameraContext()
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          src: res.tempImagePath,
          hidden: false
        })
        var _this = this
        const uploadTask = wx.uploadFile({
          url: 'http://localhost:8080/myHome/face/info/facefile', //仅为示例，非真实的接口地址
          filePath: res.tempImagePath,
          name: 'file',
          formData: {
          },
          success: function (res) {
            var data = res.data
            _this.setData({
              hidden: true
            })
            console.log(data);
          }
        })
      }
    })
  }
  ,
  endTakePhoto() {
    const ctx = wx.createCameraContext()
    this.setData({
      src: '', imglist: [], hidden: false
    })
    var _this = this;
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        var _this1 = _this;
        const uploadTask = wx.uploadFile({
          url: 'http://localhost:8080/myHome/face/info/validatefacefile', //仅为示例，非真实的接口地址
          filePath: res.tempImagePath,
          name: 'file',
          formData: {
          },
          success: function (res) {
            var urllistv = []
            console.log(res.data)
            var datav = JSON.parse(res.data).data;
            console.log(datav)
            if (datav.length > 0) {
              for (var i = 0; i < datav.length; i++) {
                var zsdz = 'http://localhost:8080/myHome/face/info/getImage?url=' + datav[i].url;
                urllistv[i] = zsdz;
              }
              _this1.setData({
                imglist: urllistv, hidden: true
              })
            } else {

            }
          }
        })


      }
    })
  }
  // tap: function (e) {
  //   for (var i = 0; i < order.length; ++i) {
  //     if (order[i] === this.data.toView) {
  //       this.setData({
  //         toView: order[i + 1]
  //       })
  //       break
  //     }
  //   }
  // },
  // tapMove: function (e) {
  //   this.setData({
  //     scrollTop: this.data.scrollTop + 10
  //   })
  // }
})