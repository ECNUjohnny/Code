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
    "   FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);\n"
    "}\n";

void CharacterCallBack(GLFWwindow* window, unsigned int codepoint)
{
    switch(codepoint)
    {
        
    }
}

int main() 
{
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
    glLineWidth(4.0f);

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