#version 330

in vec2 fragTexCoord;
in vec4 fragColor;

uniform sampler2D texture0;

uniform float time;

out vec4 finalColor;

void main() {
    float waveFactorX = sin(fragTexCoord.y * 3.0 + time * 1.5) * 0.025;
    float waveFactorY = sin(fragTexCoord.x * 3.0 + time * 1.5) * 0.025;

    vec4 texelColor = texture(texture0, fragTexCoord + vec2(waveFactorX, waveFactorY));

    finalColor = texelColor * fragColor;
}