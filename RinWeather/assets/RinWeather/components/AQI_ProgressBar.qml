import QtQuick 2.15
import QtQuick.Controls 2.15
import RinUI


ProgressBar {
    id: aqiBar
    // Layout.fillWidth: true
    // Layout.alignment: Qt.AlignBottom
    property int aqi: 0
    value: aqi / 500

    contentItem: Item {
        id: barContent
        width: parent.width
        height: parent.height

        Item {
            id: clipper
            width: aqiBar.visualPosition * barContent.width
            height: barContent.height
            clip: true

            // 动画
            Behavior on width {
                NumberAnimation { duration: Utils.animationSpeed; easing.type: Easing.OutQuint }
            }

            Rectangle {
                width: barContent.width
                height: barContent.height
                radius: 999
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "#00E400" }
                    GradientStop { position: 0.2; color: "#FFFF00" }
                    GradientStop { position: 0.4; color: "#FF7E00" }
                    GradientStop { position: 0.6; color: "#FF0000" }
                    GradientStop { position: 0.8; color: "#99004C" }
                    GradientStop { position: 1.0; color: "#7E0023" }
                }
            }
        }
    }
}