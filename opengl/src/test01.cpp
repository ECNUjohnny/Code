#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <gtc/matrix_transform.hpp>
#include <gtc/type_ptr.hpp>
#include <glm.hpp>
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <sstream>

const int N = 1005;
using namespace std;
using namespace glm;

int n, op;
float xmax = -1e9, xmin = 1e9, ymax = -1e9, ymin = 1e9;
struct vertex
{
    float x, y;
} v[N];

struct edge
{
    vertex st, en;
} e[N];

glm::mat4 Projection = glm::ortho(-400.0f, 400.0f, -400.0f, 400.0f);
glm::mat4 V, Current, I;
ifstream fin;

const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec2 aPos;\n"
    "uniform mat4 Projection;\n"
    "uniform mat4 Current;\n"
    "out vec4 transformPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = Projection * Current * vec4(aPos, 0.0, 1.0);\n"
    "   transformPos = Current * vec4(aPos, 0.0, 1.0);\n"
    "}\n";

const char *fragmentShaderSource = "#version 330 core\n"
    "in vec4 transformPos;\n"
    "out vec4 FragColor;\n"
    "void main()\n"
    "{\n"
    "   if (transformPos.x < -390 || transformPos.x > 390 || transformPos.y < -390 || transformPos.y > 390) discard;\n"
    "   FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);\n"
    "}\n";

inline int Init()
{
    scanf("%d", &n); 
    for (int i = 1; i <= n; i++)
    {
        scanf("%f%f", &v[i].x, &v[i].y);
        xmax = std::max(xmax, v[i].x);
        ymax = std::max(ymax, v[i].y);
        xmin = std::min(xmin, v[i].x);
        ymin = std::min(ymin, v[i].y);
    }
    float len = std::max(ymax - ymin, xmax - xmin);
    if (ymax - ymin != len) ymax = ymin + len;
    if (xmax - xmin != len) xmax = xmin + len;
    
    float cx = (xmax + xmin) / 2;
    float cy = (ymax + ymin) / 2;
    float S = 800.0f / len;
    
    V = mat4(1.0f);
    V = scale(V, vec3(S, S, 1.0f));
    V = translate(V, vec3(-cx, -cy, 0.0));
    Current = V;
    return 0;
}

inline void translate1()
{
    I = mat4(1.0f);
    I = translate(I, vec3(10.0f, 0, 0));
    Current = I * Current;
}

inline void translate2()
{
    I = mat4(1.0f);
    I = translate(I, vec3(-10.0f, 0, 0));
    Current = I * Current;
}

inline void translate3()
{
    I = mat4(1.0f);
    I = translate(I, vec3(0, 10.0f, 0));
    Current = I * Current;
}

inline void translate4()
{
    I = mat4(1.0f);
    I = translate(I, vec3(0, -10.0f, 0));
    Current = I * Current;
}

inline void rotate1()
{
    I = mat4(1.0f);
    I = rotate(I, radians(10.0f), vec3(0, 0, 1.0f));
    Current = I * Current;
}

inline void rotate2()
{
    I = mat4(1.0f);
    I = rotate(I, radians(-10.0f), vec3(0, 0, 1.0f));
    Current = I * Current;
}

inline void scale1()
{
    I = mat4(1.0f);
    I = scale(I, vec3(2.0f, 2.0f, 2.0f));
    Current = I * Current;
}

inline void scale2()
{
    I = mat4(1.0f);
    I = scale(I, vec3(0.5f, 0.5f, 0.5f));
    Current = I * Current;
}

void CharacterCallBack(GLFWwindow* window, unsigned int codepoint)
{
    switch(codepoint)
    {
        case 'x':
            translate1();
            break;
        case 'X':
            translate2();
            break;
        case 'y':
            translate3();
            break;
        case 'Y':
            translate4();
            break;
        case 'r':
            rotate1();
            break;
        case 'R':
            rotate2();
            break;
        case 's':
            scale1();
            break;
        case 'S':
            scale2();
            break;
        case 'h':
            Current = V;
            break;
        case 'q':
            exit(0);
        default: 
            break;
    }
}

int main() 
{
    if (Init() == -1) return 0;
    
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(1200, 1200, "Transformation", nullptr, nullptr);
    glfwMakeContextCurrent(window);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    glfwSetCharCallback(window, CharacterCallBack);

    unsigned int VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, n * sizeof(vertex), &v[1], GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(vertex), (void*)0);
    glEnableVertexAttribArray(0);

    float borderVertices[] = 
    {
        -390.0f, -390.0f,
         390.0f, -390.0f,
         390.0f,  390.0f,
        -390.0f,  390.0f
    };

    unsigned int borderVAO, borderVBO;
    glGenVertexArrays(1, &borderVAO);
    glGenBuffers(1, &borderVBO);
    glBindVertexArray(borderVAO);
    glBindBuffer(GL_ARRAY_BUFFER, borderVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(borderVertices), borderVertices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    unsigned int vert = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vert, 1, &vertexShaderSource, NULL);
    glCompileShader(vert);

    unsigned int frag = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(frag, 1, &fragmentShaderSource, NULL);
    glCompileShader(frag);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vert);
    glAttachShader(shaderProgram, frag);
    glLinkProgram(shaderProgram);

    glDeleteShader(frag);
    glDeleteShader(vert);

    int vertexCurrentLocation = glGetUniformLocation(shaderProgram, "Current");
    int vertexProjectLocation = glGetUniformLocation(shaderProgram, "Projection");
    glUseProgram(shaderProgram);
    glUniformMatrix4fv(vertexCurrentLocation, 1, GL_FALSE, glm::value_ptr(Current));
    glUniformMatrix4fv(vertexProjectLocation, 1, GL_FALSE, glm::value_ptr(Projection));

    glPointSize(7.0f);
    glLineWidth(2.0f);

    while (!glfwWindowShouldClose(window)) 
    {
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);

        glm::mat4 identityMatrix = glm::mat4(1.0f); 
        glUniformMatrix4fv(vertexCurrentLocation, 1, GL_FALSE, glm::value_ptr(identityMatrix));
        glBindVertexArray(borderVAO);
        glDrawArrays(GL_LINE_LOOP, 0, 4);

        glUniformMatrix4fv(vertexCurrentLocation, 1, GL_FALSE, glm::value_ptr(Current));
        glBindVertexArray(VAO);
        glDrawArrays(GL_LINES, 0, n);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    glfwTerminate();
    return 0;
}