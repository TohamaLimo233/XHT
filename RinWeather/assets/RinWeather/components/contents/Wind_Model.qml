import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


RowLayout {
    id: windModel

    property var windspeed: 0
    property var winspeedunit: ""
    property var winddirection: 0
    spacing: 12

    Wind_Compass {
        id: windCompass
        Layout.alignment: Qt.AlignCenter
        alwaysDark: true
        size: 80
        angle: windModel.winddirection
        value: windModel.windspeed
        description: windModel.winspeedunit

        HoverHandler {
            id: hoverHandler
        }

        ToolTip {
            visible: hoverHandler.hovered
            delay: 200
            text: qsTr(
                "Wind Speed: " + windModel.windspeed + windModel.winspeedunit + "\n" +
                "Wind Direction: " + windModel.winddirection + "°"
            )
        }
    }

    ColumnLayout {
        visible: parent.width > 200
        Layout.fillWidth: true
        RowLayout {
            Layout.fillWidth: true
            Text {
                Layout.fillWidth: true
                color: Colors.dark.textColor
                text: qsTr("Speed")
            }
            Text {
                typography: Typography.BodyStrong
                color: Colors.dark.textSecondaryColor
                text: windModel.windspeed + " " + windModel.winspeedunit
            }
        }
        MenuSeparator {
            Layout.fillWidth: true
        }
        RowLayout {
            Layout.fillWidth: true
            Text {
                Layout.fillWidth: true
                color: Colors.dark.textColor
                text: qsTr("Direction")
            }
            Text {
                typography: Typography.BodyStrong
                color: Colors.dark.textSecondaryColor
                text: windModel.winddirection + "°"
            }
        }
    }
}