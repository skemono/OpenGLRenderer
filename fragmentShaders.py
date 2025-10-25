# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


toon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    if (intensity < 0.33)
        intensity = 0.2;
    else if (intensity < 0.66)
        intensity = 0.6;
    else
        intensity = 1.0;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


negative_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;

void main()
{
    fragColor = 1 - texture(tex0, fragTexCoords);
}

'''


magma_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;

uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
    fragColor += texture(tex1, fragTexCoords) * ((sin(time) + 1) / 2);
}

'''


chromatic_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec2 center = vec2(0.5, 0.5);
    vec2 offset = fragTexCoords - center;
    float dist = length(offset);
    
    float aberration = 0.08 + sin(time * 2.0) * 0.04;
    
    float r = texture(tex0, fragTexCoords + offset * aberration * 1.5).r;
    float g = texture(tex0, fragTexCoords + offset * aberration * 0.5).g;
    float b = texture(tex0, fragTexCoords - offset * aberration * 1.0).b;
    
    vec3 colorShift = vec3(r * 1.2, g, b * 1.3);
    
    fragColor = vec4(colorShift, 1.0) * intensity;
}

'''


psychedelic_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform float time;

void main()
{
    vec3 rainbowColor;
    float hue = fract(fragTexCoords.x + fragTexCoords.y + time * 0.2);
    
    float h = hue * 6.0;
    float x = 1.0 - abs(mod(h, 2.0) - 1.0);
    
    if (h < 1.0)      rainbowColor = vec3(1.0, x, 0.0);
    else if (h < 2.0) rainbowColor = vec3(x, 1.0, 0.0);
    else if (h < 3.0) rainbowColor = vec3(0.0, 1.0, x);
    else if (h < 4.0) rainbowColor = vec3(0.0, x, 1.0);
    else if (h < 5.0) rainbowColor = vec3(x, 0.0, 1.0);
    else              rainbowColor = vec3(1.0, 0.0, x);
    
    vec4 texColor = texture(tex0, fragTexCoords);
    fragColor = vec4(texColor.rgb * rainbowColor, 1.0);
}

'''


glitch_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max(0, dot(fragNormal, lightDir)) + ambientLight;
    
    vec2 uv = fragTexCoords;
    
    float glitchLine = step(0.98, sin(uv.y * 100.0 + time * 20.0));
    uv.x += glitchLine * sin(time * 50.0) * 0.1;
    
    float blockNoise = fract(sin(floor(uv.y * 10.0) * 12.9898 + time) * 43758.5453);
    if (blockNoise > 0.95) {
        uv.x += sin(time * 30.0) * 0.05;
    }
    
    vec4 texColor = texture(tex0, uv);
    
    float scanline = sin(uv.y * 800.0) * 0.1;
    texColor.rgb += scanline;
    
    fragColor = texColor * intensity;
}

'''




