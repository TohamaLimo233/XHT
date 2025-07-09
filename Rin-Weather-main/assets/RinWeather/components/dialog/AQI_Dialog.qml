import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


Dialog {
    id: aqiDialog
    title: qsTr("Air Quality")
    modal: true

    property var aqi: 0

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
            spacing: 12
            Text {
                Layout.alignment: Qt.AlignTop
                typography: Typography.BodyStrong
                text: WeatherResource.getAQICategory(aqi)
            }
            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    Text {
                        text: qsTr("Current AQI is " + aqi + ".")
                    }
                    AQI_ProgressBar {
                        Layout.fillWidth: true
                        aqi: aqiDialog.aqi
                    }
                }
            }

            Text {
                Layout.alignment: Qt.AlignTop
                typography: Typography.BodyStrong
                text: qsTr("Health Information")
            }
            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    width: parent.width
                    spacing: 12
                    Text {
                        Layout.fillWidth: true
                        text: WeatherResource.getAQIInfo(aqi)
                    }
                    Text {
                        Layout.fillWidth: true
                        text: WeatherResource.getAQIAdvice(aqi)
                    }
                }
            }
        }
    }

    standardButtons: Dialog.Ok
}