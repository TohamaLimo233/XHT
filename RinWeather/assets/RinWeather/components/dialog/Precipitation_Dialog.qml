import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather
import QtCharts 2.15


Dialog {
    id: precipitationDialog
    title: qsTr("Precipitation")
    modal: true

    property var precipitation: 0
    property var model: []

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
                typography: Typography.BodyLarge
                text: precipitationDialog.precipitation
            }
            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12
                    Text {
                        text: qsTr("Total for the day")
                    }

                    Flickable {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 220
                        contentWidth: precipitationChart.width
                        clip: true

                        ScrollBar.horizontal: ScrollBar { }

                        Precipitation_Chart {
                            id: precipitationChart
                            width: 1200
                            height: parent.height
                            model: precipitationDialog.model
                        }
                    }
                }
            }
        }
    }

    standardButtons: Dialog.Ok
}