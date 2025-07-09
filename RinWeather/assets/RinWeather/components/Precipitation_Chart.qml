import QtQuick 2.15
import QtQuick.Controls 2.15
import QtCharts 2.15
import RinUI
import RinWeather


ChartView {
    id: chartView

    // 样式
    legend.visible: false
    margins { left: 0; right: 0; top: 0; bottom: 0 }
    antialiasing: true

    backgroundColor: "transparent"

    property var model

    property var categories
    property var values
    property int maxValue: 10

    Component.onCompleted: {
        parserData(model)
    }
    onModelChanged: {
        parserData(model)
    }


    // 解析数据
    function parserData(model) {
        let categories = []
        let values = []
        let value

        maxValue = 10

        for (var i = 0; i < model.length; i++) {
            categories.push(model[i].time)
            value = parseFloat(model[i].precipitation.split(" ", 2)[0])
            if (value > maxValue) {
                chartView.maxValue = value + value * 0.2
            }
            values.push(value)
        }

        chartView.categories = categories
        chartView.values = values
    }

    // X坐标轴
    BarCategoryAxis {
        id: xAxis
        gridLineColor: Colors.proxy.controlBorderColor
        labelsColor: Colors.proxy.textColor
        categories: chartView.categories
        color: Colors.proxy.controlBorderColor
        // categories: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    }

    // Y坐标轴
    ValueAxis {
        id: yAxis
        min: 0
        max: maxValue
        labelsVisible: false
        gridLineColor: Colors.proxy.controlBorderColor
        color: Colors.proxy.controlBorderColor
    }

    BarSeries {
        id: precipitationSeries
        axisX: xAxis
        axisY: yAxis
        labelsVisible: true
        labelsPosition: BarSeries.LabelsOutsideEnd

        BarSet {
            color: RinColor.precipitationColor
            labelColor: Colors.proxy.textSecondaryColor
            borderColor: "transparent"
            values: chartView.values
            // values: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        }
    }
}