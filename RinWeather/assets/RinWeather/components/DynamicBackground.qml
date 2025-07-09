import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Particles 2.15
import Qt5Compat.GraphicalEffects
import RinWeather

Item {
    id: root
    property real currentHour: new Date().getHours() + new Date().getMinutes() / 60
    property var gradientColors: TimeColorUtil.getGradientByHour(currentHour)
    property int duration: 1200 // 动画持续时间

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop {
                position: 0.0; color: root.gradientColors.top
                Behavior on color {
                    ColorAnimation {
                        duration: root.duration
                        easing.type: Easing.OutQuad
                    }
                }
            }
            GradientStop {
                position: 1.0; color: root.gradientColors.bottom
                Behavior on color {
                    ColorAnimation {
                        duration: root.duration
                        easing.type: Easing.OutQuad
                    }
                }
            }
        }
        Component.onCompleted: {
            console.log(root.gradientColors)
        }
    }

    // 噪声
    Item {
        id: scroller
        width: parent.width * 2
        height: parent.height
        opacity: 0.05
        x: scrollX
        property real scrollX: 0

        Image {
            source: RinPath.assets("resources/images/noise.png")
            anchors.left: parent.left
            fillMode: Image.PreserveAspectCrop
            width: parent.width / 2
            height: parent.height
        }

        Image {
            source: RinPath.assets("resources/images/noise.png")
            anchors.right: parent.right
            x: parent.width / 2
            fillMode: Image.PreserveAspectCrop
            width: parent.width / 2
            height: parent.height
        }

        SequentialAnimation on scrollX {
            id: scrollAnim
            loops: Animation.Infinite
            PropertyAnimation {
                from: 0
                to: -parent.width
                duration: (parent.width / 100) * 1000
                easing.type: Easing.Linear
            }
        }
         onWidthChanged: {
            scrollAnim.stop()
            scrollAnim.animations[0].to = -parent.width
            scrollAnim.animations[0].duration = (parent.width / 25) * 1000
            scrollX = 0 // 重置位置
            scrollAnim.start()
        }
    }

    // 可选粒子层 / 云层放这里
}
