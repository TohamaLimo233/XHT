import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI
import RinWeather


ColumnLayout {
    id: apparentTempModel

    property var temperature: 0

    Text {
        Layout.alignment: Qt.AlignBottom
        typography: Typography.Subtitle
        color: Colors.dark.textColor
        text: temperature + "°"
    }
}