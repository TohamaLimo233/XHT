pragma Singleton
import QtQuick 2.15

QtObject {
    id: util

    property var gradientPoints: [
        { hour: 5, colorTop: "#090f1f", colorBottom: "#1b1f2a" },
        { hour: 6, colorTop: "#245490", colorBottom: "#b4b8ce" },
        { hour: 9, colorTop: "#0f53ab", colorBottom: "#9dc1f0" },
        { hour: 12, colorTop: "#245f98", colorBottom: "#63a3e3" },
        { hour: 13, colorTop: "#103a7a", colorBottom: "#6b9ccd" },
        { hour: 16, colorTop: "#245f98", colorBottom: "#63a3e3" },
        { hour: 19, colorTop: "#224071", colorBottom: "#d4ab94" },
        { hour: 20, colorTop: "#242f4d", colorBottom: "#5a4d61" },
        { hour: 21, colorTop: "#090f1f", colorBottom: "#1b1f2a" }
    ]

    function hexToRgb(hex) {
        hex = hex.replace("#", "")
        const bigint = parseInt(hex, 16)
        return Qt.rgba(
            ((bigint >> 16) & 255) / 255,
            ((bigint >> 8) & 255) / 255,
            (bigint & 255) / 255,
            1.0
        )
    }

    function lerpColor(c1, c2, t) {
        return Qt.rgba(
            c1.r + (c2.r - c1.r) * t,
            c1.g + (c2.g - c1.g) * t,
            c1.b + (c2.b - c1.b) * t,
            1.0
        )
    }

    function getGradientByHour(hour) {
        for (let i = 0; i < gradientPoints.length - 1; i++) {
            const a = gradientPoints[i]
            const b = gradientPoints[i + 1]
            if (hour >= a.hour && hour <= b.hour) {
                const t = (hour - a.hour) / (b.hour - a.hour)
                return {
                    top: lerpColor(hexToRgb(a.colorTop), hexToRgb(b.colorTop), t),
                    bottom: lerpColor(hexToRgb(a.colorBottom), hexToRgb(b.colorBottom), t)
                }
            }
        }
        return {
            top: hexToRgb(gradientPoints[0].colorTop),
            bottom: hexToRgb(gradientPoints[0].colorBottom)
        }
    }
}
