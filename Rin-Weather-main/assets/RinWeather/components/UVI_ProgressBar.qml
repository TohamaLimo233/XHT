import QtQuick 2.15
import QtQuick.Controls 2.15
import RinUI


ProgressBar {
    id: uviBar
    // Layout.fillWidth: true
    // Layout.alignment: Qt.AlignBottom
    property int uvi: 0
    value: Math.min(uvi / 11, 11)

    background: Item {
        width: parent.width
        height: 1

        Rectangle {
            id: gradientBg
            anchors.fill: parent
            radius: 999
            opacity: 0.5
            visible: uviBar.value === 0

            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "#3ea72d" }
                GradientStop { position: 0.25; color: "#fff300" }
                GradientStop { position: 0.50; color: "#f18b00" }
                GradientStop { position: 0.75; color: "#e53210" }
                GradientStop { position: 1.0; color: "#b567a4" }
            }
        }

        Rectangle {
            id: solidBg
            anchors.fill: parent
            radius: 999
            opacity: 0.5
            color: Colors.proxy.controlBorderStrongColor
            visible: uviBar.value !== 0
        }
    }

    contentItem: Item {
        id: barContent
        width: parent.width
        height: parent.height

        Item {
            id: clipper
            width:uviBar.visualPosition * barContent.width
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
                    GradientStop { position: 0.0; color: "#3ea72d" }
                    GradientStop { position: 0.25; color: "#fff300" }
                    GradientStop { position: 0.50; color: "#f18b00" }
                    GradientStop { position: 0.75; color: "#e53210" }
                    GradientStop { position: 1.0; color: "#b567a4" }
                }
            }
        }
    }
}