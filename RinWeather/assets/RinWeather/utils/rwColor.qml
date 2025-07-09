pragma Singleton
import QtQuick 2.15

QtObject {
    // Colors //
    property color temperatureColor: "#fe701d"
    property color precipitationColor: "#63cefa"
    property color weatherColor: "#63a4fa"
    property color sunProgressColor: "#f6cc8c"
    property var temperatureGradient: Gradient {
        orientation: Gradient.Horizontal
        GradientStop { position: 0.0; color: "#ff8515" }
        GradientStop { position: 1.0; color: "#ff562b" }
    }
}