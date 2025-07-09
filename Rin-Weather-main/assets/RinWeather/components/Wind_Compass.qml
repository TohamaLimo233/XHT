import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

Item {
    id: compassRing
    implicitWidth: size
    implicitHeight: size

    property bool alwaysDark: false

    property int size: 100
    readonly property int tickCount: 360 / compassRing.tickAngle
    property real tickAngle: 5
    property real radius: width / 2

    property real angle: 0
    property var value: angle
    property string description: "Degrees"

    // pointer
    Image {
        anchors.fill: parent
        source: RinPath.resources("images/components/wind_arrow.svg")
        fillMode: Image.PreserveAspectFit
        smooth: true
        rotation: compassRing.angle
    }

    // contents
    ColumnLayout {
        anchors.centerIn: parent
        x: -2
        spacing: 0

        Text {
            Layout.alignment: Qt.AlignHCenter
            color: alwaysDark ? Colors.dark.textColor : Colors.proxy.textColor
            typography: Typography.BodyStrong
            text: compassRing.value
        }
        Text {
            Layout.alignment: Qt.AlignHCenter
            typography: Typography.Caption
            // font.pixelSize: 10
            color: alwaysDark ? Colors.dark.textColor : Colors.proxy.textColor
            text: compassRing.description
        }
    }


    // 圆环
    Repeater {
        model: compassRing.tickCount

        delegate: Rectangle {
            id: tick

            property int mainStep: compassRing.tickCount / 4

            property int range: 2

            // 是否为主方向
            property bool isMainDir: (index % mainStep) === 0

            function circularDistance(a, b, max) {
                let diff = Math.abs(a - b);
                return Math.min(diff, max - diff);
            }

            // 是否为临近主方向
            property bool isNearMainDir: {
                if (isMainDir) return false;
                let nearestMainDirIndex = Math.round(index / mainStep) * mainStep;
                let dist = circularDistance(index, nearestMainDirIndex, compassRing.tickCount);
                return dist <= range;
            }

            width: 1
            height: 8

            color: isMainDir || isNearMainDir ? "transparent"
                : index % (compassRing.tickCount / 12) === 0
                ? alwaysDark ? Colors.dark.controlBorderStrongColor : Colors.proxy.controlBorderStrongColor
                : alwaysDark ? Colors.dark.controlBorderColor : Colors.proxy.controlBorderColor

            radius: 1
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                typography: Typography.Caption
                color: alwaysDark ? Colors.dark.textSecondaryColor : Colors.proxy.textSecondaryColor
                visible: isMainDir
                rotation: -rotation.angle

                text: {
                    if (index === 0) return "N"
                    if (index === compassRing.tickCount/4) return "E"
                    if (index === compassRing.tickCount/2) return "S"
                    if (index === compassRing.tickCount*3/4) return "W"
                    return ""
                }

                anchors.centerIn: parent
            }

            transform: [
                Rotation {
                    id: rotation
                    origin.x: 0
                    origin.y: compassRing.radius
                    angle: index * tickAngle
                },
                Translate { x: 0; y: -compassRing.radius + tick.height / 2 }
            ]
        }
    }
}
