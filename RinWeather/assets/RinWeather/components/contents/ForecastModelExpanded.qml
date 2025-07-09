import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather

Flickable {
    id: forecastModel
    clip: true

    property alias model: rpt.model

    property real minTemp: Math.min.apply(null, rpt.model.map(x => x.l_temp))
    property real maxTemp: Math.max.apply(null, rpt.model.map(x => x.h_temp))

    contentHeight: modelLayout.height

    ColumnLayout {
        id: modelLayout
        width: parent.width
        spacing: 8

        Repeater {
            id: rpt

            model: {}
            //     let example = [];
            //     for (let i = 0; i < 7; i++) {
            //         example.push({
            //             time: i,
            //             code: 0,
            //             h_temp: 22 + i,
            //             l_temp: 20 + i,
            //         });
            //     }
            //     return example;
            // }

            delegate: RowLayout {
                Layout.preferredHeight: 36
                Layout.fillWidth: true
                spacing: 12

                Text {
                    Layout.preferredWidth: 50
                    color: Colors.dark.textColor
                    typography: Typography.Body
                    Layout.alignment: Qt.AlignHCenter
                    text: modelData.time
                }

                Item { Layout.fillWidth: true }

                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredHeight: 28
                    spacing: 0
                    Image {
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        Layout.preferredWidth: 32
                        Layout.preferredHeight: 24
                        source: WeatherResource.getWeatherImage(modelData.code)
                        fillMode: Image.PreserveAspectFit
                    }
                    Text {
                        color: RinColor.precipitationColor
                        font.bold: true
                        Layout.alignment: Qt.AlignHCenter
                        typography: Typography.Caption
                        font.pixelSize: 11
                        text: modelData.precipitation
                        visible: modelData.precipitation !== "None"
                    }

                    HoverHandler { id: weatherHandler }
                    ToolTip {
                        id: toolTip
                        text: WeatherResource.getWeatherDescription(modelData.code)
                        visible: weatherHandler.hovered
                    }
                }

                Item { Layout.fillWidth: true }

                RowLayout {
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
                    spacing: 4

                    Text {
                        typography: Typography.BodyStrong
                        color: Colors.dark.textSecondaryColor
                        text: modelData.l_temp + "°"
                    }

                    // Temperature bar / 温度条 //
                    Rectangle {
                        id: barBg
                        width: 100
                        height: 4
                        radius: 2
                        color: Colors.proxy.controlAltQuaternaryColor

                        property real startRatio: (modelData.l_temp - forecastModel.minTemp)
                            / (forecastModel.maxTemp - forecastModel.minTemp)
                        property real endRatio: (modelData.h_temp - forecastModel.minTemp)
                            / (forecastModel.maxTemp - forecastModel.minTemp)

                        Rectangle {
                            id: indicator
                            x: barBg.width * barBg.startRatio
                            width: barBg.width * (barBg.endRatio - barBg.startRatio)
                            height: parent.height
                            radius: parent.radius
                            gradient: RinColor.temperatureGradient
                        }
                    }

                    Text {
                        color: Colors.dark.textColor
                        typography: Typography.BodyStrong
                        text: modelData.h_temp + "°"
                    }
                }
            }
        }
    }
}
