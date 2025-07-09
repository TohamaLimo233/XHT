import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather
import QtCharts 2.15


Dialog {
    id: weatherDialog
    title: qsTr("Weather Condition")
    modal: true

    property var currentWeather: {}
    property var model: {}

    spacing: 4

    Flickable {
        Layout.fillWidth: true
        Layout.preferredHeight: Math.min(contentLayout.height, parent.height)
        contentHeight: contentLayout.height
        clip: true

        ScrollBar.vertical: ScrollBar { }

        ColumnLayout {
            id: contentLayout
            width: parent.width
            spacing: 6

            RowLayout {
                Layout.fillWidth: true

                ColumnLayout {
                    spacing: 0
                    RowLayout {
                        spacing: 4
                        Text {
                            Layout.alignment: Qt.AlignVCenter
                            typography: Typography.BodyLarge
                            text: Math.round(currentWeather["temperature"]) + "°"
                        }
                        Image {
                            Layout.preferredWidth: 28
                            Layout.preferredHeight: 28
                            source: WeatherResource.getWeatherImage(currentWeather["weathercode"])
                            fillMode: Image.PreserveAspectFit
                        }
                    }
                    Text {
                        Layout.alignment: Qt.AlignTop
                        typography: Typography.Body
                        color: Colors.proxy.textSecondaryColor
                        text: qsTr("H:" + currentTemperatures[0] + "° L:" + currentTemperatures[1] + "°")
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

                Segmented {
                    id: segmented
                    Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                    SegmentedItem {
                        icon.name: "ic_fluent_temperature_20_regular"
                    }
                    SegmentedItem {
                        icon.name: "ic_fluent_weather_partly_cloudy_day_20_regular"
                    }
                }
            }
            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    Flickable {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 220
                        contentWidth: weatherChart.width
                        clip: true

                        ScrollBar.horizontal: ScrollBar { }

                        Weather_Chart {
                            id: weatherChart
                            width: 1200
                            height: parent.height
                            model: weatherDialog.model

                            labelVisible: {
                                switch (segmented.currentIndex) {
                                    case 0: return true
                                    case 1: return false
                                }
                            }

                            modelKey: {
                                switch (segmented.currentIndex) {
                                    case 0: return "temperature"
                                    case 1: return "code"
                                }
                            }

                            themeColor: {
                                switch (segmented.currentIndex) {
                                    case 0: return RinColor.temperatureColor
                                    case 1: return RinColor.weatherColor
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    standardButtons: Dialog.Ok
}