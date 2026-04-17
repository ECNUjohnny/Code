#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 Projection;

void main()
{
    gl_Position = Projection * vec4(aPos, 1.0f);
}