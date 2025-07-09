import QtQuick 2.15
import QtQuick.Controls 2.15
import QtCharts 2.15
import RinUI

ChartView {
    id: chartView

    legend.visible: false
    margins { left: 0; right: 0; top: 0; bottom: 0 }
    antialiasing: true
    backgroundColor: "transparent"

    property var model
    property var modelKey: "temperature"
    property var categories
    property var oldCategories
    property var values
    property bool labelVisible: true
    property string unit: "°"
    property int maxValue: 15
    property int minValue: 10
    property color themeColor: RinColor.temperatureColor

    Component.onCompleted: {
        parserData(model)
    }
    onModelChanged: {
        parserData(model)
    }

    onModelKeyChanged: {
        parserData(model)
    }

    function parserData(model) {
        let categories = []
        let oldCategories = chartView.oldCategories || []
        let values = []
        let value

        maxValue = 15
        minValue = 10

        for (var i = 0; i < model.length; i++) {
            categories.push(model[i].time)
            value = parseFloat(model[i][modelKey])
            if (value > maxValue) {
                chartView.maxValue = value + value * 0.2
            }
            if (value < minValue) {
                chartView.minValue = value - value * 0.2
            }
            values.push(value)
        }

        chartView.categories = categories
        chartView.values = values

        // 更新坐标轴范围
        for (let d = 0; d < oldCategories.length; d++) {
            xAxis.remove(oldCategories[d])
        }
        xAxis.min = 0
        xAxis.max = values.length - 1
        for (let i = 0; i < categories.length; i++) {
            xAxis.append(categories[i], i)
        }
        chartView.oldCategories = categories

        splineSeries.clear()
        for (let j = 0; j < values.length; j++) {
            splineSeries.append(j, values[j])
        }
    }

    CategoryAxis {
        id: xAxis
        labelsColor: Colors.proxy.textColor
        gridLineColor: Colors.proxy.controlBorderColor
        color: Colors.proxy.controlBorderColor
        min: 0
        max: 1
    }

    ValueAxis {
        id: yAxis
        min: minValue
        max: maxValue
        labelsColor: Colors.proxy.textSecondaryColor
        gridLineColor: Colors.proxy.controlBorderColor
        color: Colors.proxy.controlBorderColor
    }

    SplineSeries {
        id: splineSeries
        axisX: xAxis
        axisY: yAxis

        color: themeColor
        width: 2
        pointsVisible: true
        pointLabelsVisible: chartView.labelVisible
        pointLabelsFont.pixelSize: 14
        pointLabelsFormat: "@yPoint" + unit
        pointLabelsColor: Colors.proxy.textSecondaryColor
    }
}
