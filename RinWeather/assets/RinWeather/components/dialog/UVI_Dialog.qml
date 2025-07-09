import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


Dialog {
    id: uviDialog
    title: qsTr("UV Index")
    modal: true

    property var uvi: 0

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
                text: WeatherResource.getUVICategory(uvi)
            }
            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    Text {
                        text: qsTr("Current UVI is " + uvi + ".")
                    }
                    UVI_ProgressBar {
                        Layout.fillWidth: true
                        uvi: uviDialog.uvi
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
                        text: WeatherResource.getUVIInfo(uvi)
                    }
                    Text {
                        Layout.fillWidth: true
                        text: WeatherResource.getUVIAdvice(uvi)
                    }
                }
            }
        }
    }

    standardButtons: Dialog.Ok
}