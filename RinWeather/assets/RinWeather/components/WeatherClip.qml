import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI


Clip {
    id: root
    radius: Appearance.proxy.buttonRadius

    default property alias content: contentsArea.data

    // dark style
    color: Colors.dark.controlFillSecondaryColor
    borderColor: Colors.dark.cardBorderColor

    Layout.fillWidth: true
    implicitWidth: 200
    implicitHeight: 150

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 8

        RowLayout {
            spacing: 6
            IconWidget {
                id: iconLabel
                size: 18
                color: Colors.dark.textSecondaryColor
                icon: root.icon.name
            }
            Text {
                id: titleLabel
                typography: Typography.Caption
                color: Colors.dark.textSecondaryColor
                text: root.text
            }
        }

        // 插槽式内容
        Item {
            id: contentsArea
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    // property alias title: titleLabel.text
}
