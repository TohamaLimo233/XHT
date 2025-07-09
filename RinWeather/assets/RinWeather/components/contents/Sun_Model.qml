import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


ColumnLayout {
    id: sunModel

    property double currentHour: 12
    property var sunrise: "6:00"
    property var sunset: "18:00"

    ProgressBar {
        Layout.fillWidth: true
        value: currentHour
        from: 0
        to: 24
        primaryColor: RinColor.sunProgressColor
    }

    Item {
        Layout.fillHeight: true
    }

    RowLayout {
        Layout.alignment: Qt.AlignBottom
        spacing: 12
        Text {
            typography: Typography.Subtitle
            color: Colors.dark.textColor
            text: sunrise
        }
        Text {
            typography: Typography.Body
            color: Colors.dark.textSecondaryColor
            text: qsTr("Sunrise")
            font.bold: false
        }
    }

    RowLayout {
        Layout.alignment: Qt.AlignBottom
        spacing: 12
        Text {
            typography: Typography.Subtitle
            color: Colors.dark.textColor
            text: sunset
        }
        Text {
            typography: Typography.Body
            color: Colors.dark.textSecondaryColor
            text: qsTr("Sunset")
            font.bold: false
        }
    }
}