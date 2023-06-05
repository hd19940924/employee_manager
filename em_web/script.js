$('#open-btn').on('click', function () {
  var layerIndex = layer.open({
    title: '提示',
    content: '这是提示内容',
    btn: ['关闭'],
    yes: function (index, layero) {
      layer.close(layerIndex); // 关闭弹窗
    }
  });
});