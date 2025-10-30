# GLSL - Original Fragment Shaders Collection

# Shader 1: Glitch 
rim_lighting_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

// Random function for glitch
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float diffuse = max(0.0, dot(normal, lightDir)) + ambientLight;

    // Glitch effect: random displacement
    float glitchStrength = sin(time * 3.0) * 0.5 + 0.5;
    float glitchLine = floor(fragTexCoords.y * 20.0 + time * 5.0);
    float glitch = step(0.95, random(vec2(glitchLine, floor(time * 2.0)))) * glitchStrength;

    // Chromatic aberration with glitch
    vec2 offset = vec2(glitch * 0.03, 0.0);
    float r = texture(tex0, fragTexCoords + offset).r;
    float g = texture(tex0, fragTexCoords).g;
    float b = texture(tex0, fragTexCoords - offset).b;

    // Scanlines
    float scanline = sin(fragTexCoords.y * 300.0 + time * 10.0) * 0.5 + 0.5;
    scanline = scanline * 0.3 + 0.7;

    // Holographic rainbow shift
    float holo = sin(fragTexCoords.y * 10.0 + time * 2.0) * 0.5 + 0.5;
    vec3 holoColor = vec3(
        sin(holo * 6.28 + time),
        sin(holo * 6.28 + time + 2.09),
        sin(holo * 6.28 + time + 4.18)
    ) * 0.5 + 0.5;

    // Digital noise
    float noise = random(fragTexCoords + time) * 0.1;

    // Combine all effects
    vec3 glitchColor = vec3(r, g, b) * diffuse;
    glitchColor = mix(glitchColor, holoColor, 0.4);
    glitchColor *= scanline;
    glitchColor += noise;

    // Add intense edge glow
    vec3 viewDir = normalize(-fragPosition.xyz);
    float edge = 1.0 - abs(dot(viewDir, normal));
    edge = pow(edge, 2.0);
    glitchColor += holoColor * edge * 1.5;

    fragColor = vec4(glitchColor, 1.0);
}
'''


# Shader 2:  
fresnel_metallic_shader = '''
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
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float diffuse = max(0.0, dot(normal, lightDir)) + ambientLight;

    // Multiple plasma layers with different frequencies
    float plasma1 = sin(fragPosition.x * 2.0 + time * 3.0);
    float plasma2 = sin(fragPosition.y * 3.0 - time * 2.0);
    float plasma3 = sin(fragPosition.z * 2.5 + time * 2.5);
    float plasma4 = sin(length(fragPosition.xy) * 4.0 - time * 4.0);

    // Combine plasma waves
    float plasmaValue = (plasma1 + plasma2 + plasma3 + plasma4) / 4.0;
    plasmaValue = plasmaValue * 0.5 + 0.5; // Normalize to 0-1

    // Create fire/plasma color gradient
    vec3 color1 = vec3(0.1, 0.0, 0.3);  // Deep purple
    vec3 color2 = vec3(1.0, 0.0, 0.5);  // Hot pink
    vec3 color3 = vec3(1.0, 0.5, 0.0);  // Orange
    vec3 color4 = vec3(1.0, 1.0, 0.3);  // Yellow
    vec3 color5 = vec3(0.0, 1.0, 1.0);  // Cyan

    // Multi-stop gradient
    vec3 plasmaColor;
    if (plasmaValue < 0.2) {
        plasmaColor = mix(color1, color2, plasmaValue / 0.2);
    } else if (plasmaValue < 0.4) {
        plasmaColor = mix(color2, color3, (plasmaValue - 0.2) / 0.2);
    } else if (plasmaValue < 0.6) {
        plasmaColor = mix(color3, color4, (plasmaValue - 0.4) / 0.2);
    } else {
        plasmaColor = mix(color4, color5, (plasmaValue - 0.6) / 0.4);
    }

    // Add pulsing effect
    float pulse = sin(time * 5.0) * 0.3 + 0.7;
    plasmaColor *= pulse;

    // Mix with original texture
    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 finalColor = mix(texColor.rgb, plasmaColor, 0.7) * diffuse;

    // Add intense highlights based on normal
    vec3 viewDir = normalize(-fragPosition.xyz);
    float highlight = pow(max(0.0, dot(viewDir, normal)), 8.0);
    finalColor += plasmaColor * highlight * 2.0;

    // Add shimmer effect
    float shimmer = sin(time * 10.0 + plasmaValue * 20.0) * 0.2 + 0.8;
    finalColor *= shimmer;

    fragColor = vec4(finalColor, 1.0);
}
'''


# Shader 3: Procedural Patterns 
procedural_patterns_shader = '''
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
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float diffuse = max(0.0, dot(normal, lightDir)) + ambientLight;

    // Create animated wave patterns based on world position
    float pattern1 = sin(fragPosition.y * 2.0 + time * 2.0) * 0.5 + 0.5;
    float pattern2 = sin(fragPosition.x * 3.0 - time * 1.5) * 0.5 + 0.5;
    float pattern3 = sin(length(fragPosition.xz) * 4.0 - time * 3.0) * 0.5 + 0.5;

    // Combine patterns
    float combinedPattern = (pattern1 + pattern2 + pattern3) / 3.0;

    vec4 texColor = texture(tex0, fragTexCoords);
    vec3 patternColor = vec3(0.2, 0.8, 0.9); // Cyan pattern color

    // Mix texture with procedural pattern
    vec3 finalColor = mix(texColor.rgb, patternColor, combinedPattern * 0.4);
    finalColor *= diffuse;

    fragColor = vec4(finalColor, texColor.a);
}
'''


# Shader 4:
gooch_shading_shader = '''
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
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);

    // Calculate light intensity
    float NdotL = dot(normal, lightDir);

    vec4 texColor = texture(tex0, fragTexCoords);

    // Cool and warm colors for Gooch shading
    vec3 coolColor = vec3(0.0, 0.0, 0.6) + texColor.rgb * 0.3;
    vec3 warmColor = vec3(0.9, 0.6, 0.0) + texColor.rgb * 0.6;

    // Map light direction to cool-warm range
    float goochFactor = (1.0 + NdotL) * 0.5;
    vec3 goochColor = mix(coolColor, warmColor, goochFactor);

    // Add subtle specular highlight
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(0.0, dot(viewDir, reflectDir)), 16.0);

    vec3 finalColor = goochColor + vec3(spec * 0.3);
    fragColor = vec4(finalColor, texColor.a);
}
'''


# Shader 5: PSYCHEDELIC 
psychedelic_warp_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;
uniform float time;

// Hash function for procedural generation
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// 2D Noise
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

// Fractal Brownian Motion
float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for(int i = 0; i < 5; i++) {
        value += amplitude * noise(p);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

// HSV to RGB conversion
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

// Kaleidoscope effect
vec2 kaleidoscope(vec2 uv, float segments, float time) {
    vec2 center = vec2(0.5, 0.5);
    vec2 delta = uv - center;
    float angle = atan(delta.y, delta.x);
    float radius = length(delta);

    angle += time * 0.5;
    float segmentAngle = 6.28318 / segments;
    angle = mod(angle, segmentAngle);
    angle = abs(angle - segmentAngle * 0.5);

    return center + vec2(cos(angle), sin(angle)) * radius;
}

// Voronoi cells for fracture effect
vec2 voronoi(vec2 p) {
    vec2 n = floor(p);
    vec2 f = fract(p);

    float minDist = 1.0;
    vec2 minPoint;

    for(int j = -1; j <= 1; j++) {
        for(int i = -1; i <= 1; i++) {
            vec2 b = vec2(float(i), float(j));
            vec2 r = b + hash(n + b) - f;
            float d = length(r);
            if(d < minDist) {
                minDist = d;
                minPoint = r;
            }
        }
    }

    return vec2(minDist, hash(n + minPoint));
}

void main()
{
    vec3 normal = normalize(fragNormal);
    vec3 viewDir = normalize(-fragPosition.xyz);
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float diffuse = max(0.0, dot(normal, lightDir)) + ambientLight;

    // LAYER 1: Kaleidoscope texture distortion
    float kaleido = sin(time * 0.5) * 3.0 + 6.0;
    vec2 distortedUV = kaleidoscope(fragTexCoords, kaleido, time);

    // LAYER 2: Chromatic aberration with radial distortion
    vec2 center = vec2(0.5);
    vec2 offset = (distortedUV - center) * 0.02 * sin(time * 2.0);
    float r = texture(tex0, distortedUV + offset).r;
    float g = texture(tex0, distortedUV).g;
    float b = texture(tex0, distortedUV - offset).b;
    vec3 chromaticColor = vec3(r, g, b);

    // LAYER 3: Fractal noise overlay
    vec2 noiseCoord = fragTexCoords * 5.0 + time * 0.3;
    float fractalNoise = fbm(noiseCoord);

    // LAYER 4: Voronoi fracture cells
    vec2 voronoiCoord = fragPosition.xy * 0.5 + time * 0.2;
    vec2 voronoiData = voronoi(voronoiCoord);
    float cells = voronoiData.y;
    float edges = smoothstep(0.0, 0.1, voronoiData.x);

    // LAYER 5: Rainbow HSV cycling based on multiple parameters
    float hue = fract(
        fragTexCoords.x * 2.0 +
        fragTexCoords.y * 1.5 +
        time * 0.3 +
        fractalNoise * 0.5 +
        cells * 0.3 +
        length(fragPosition.xyz) * 0.05
    );
    vec3 rainbowColor = hsv2rgb(vec3(hue, 0.8, 1.0));

    // LAYER 6: Plasma energy waves in 3D space
    float plasma = sin(fragPosition.x * 3.0 + time * 4.0) *
                   cos(fragPosition.y * 2.5 - time * 3.0) *
                   sin(fragPosition.z * 3.5 + time * 3.5);
    plasma = plasma * 0.5 + 0.5;

    // LAYER 7: Pulsing rings emanating from model
    float dist = length(fragPosition.xyz);
    float rings = sin(dist * 5.0 - time * 8.0) * 0.5 + 0.5;
    rings = pow(rings, 3.0);

    // LAYER 8: Dissolve/glitch particles
    float dissolve = step(0.7, hash(floor(fragTexCoords * 100.0 + time * 2.0)));
    vec3 particleColor = hsv2rgb(vec3(time * 0.2, 1.0, 1.0)) * dissolve * 2.0;

    // LAYER 9: Fresnel glow with color cycling
    float fresnel = pow(1.0 - max(0.0, dot(viewDir, normal)), 3.0);
    vec3 fresnelColor = hsv2rgb(vec3(time * 0.1, 1.0, 1.0)) * fresnel * 2.0;

    // LAYER 10: Specular highlights with chromatic split
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(0.0, dot(viewDir, reflectDir)), 16.0);
    vec3 specColor = rainbowColor * spec * 3.0;

    // MEGA COMBINATION: Mix all layers with complex weighting
    vec3 finalColor = chromaticColor * diffuse;
    finalColor = mix(finalColor, rainbowColor, 0.6);
    finalColor *= (1.0 + fractalNoise * 0.8);
    finalColor = mix(finalColor, vec3(plasma) * rainbowColor, 0.4);
    finalColor += rings * rainbowColor * 0.5;
    finalColor += particleColor;
    finalColor += fresnelColor;
    finalColor += specColor;

    // Voronoi cell coloring with edges
    finalColor = mix(finalColor, rainbowColor * cells, 0.3);
    finalColor *= edges;

    // Pulsing intensity modulation
    float pulse = sin(time * 6.0) * 0.15 + 0.85;
    finalColor *= pulse;

    // Add occasional flash/strobe effect
    float strobe = step(0.98, sin(time * 20.0)) * 0.5;
    finalColor += vec3(strobe);

    // Reality warp: color inversion zones
    float warp = step(0.5, sin(fractalNoise * 10.0 + time * 2.0));
    if(warp > 0.5) {
        finalColor = vec3(1.0) - finalColor;
    }

    // Final saturation boost
    finalColor = pow(finalColor, vec3(0.9));

    fragColor = vec4(finalColor, 1.0);
}
'''




