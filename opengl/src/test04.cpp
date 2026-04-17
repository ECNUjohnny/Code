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

using namespace std;

using namespace glm;

const int N = 1e4 + 5;
unsigned int VAO, VBO, vert, frag, shaderProgram;
int m, n;
char vertShader[N], fragShader[N], ch;
FILE *file;
mat4 Projection = glm::ortho(-450.0f, 450.0f, -450.0f, 450.0f);

struct point
{
    float x, y;
} s[505], st, en;

int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *window = glfwCreateWindow(1200, 1200, "Breshham", nullptr, nullptr);
    glfwMakeContextCurrent(window);

    scanf("%f%f%f%f", st.x, st.y, en.x, en.y);
    n = en.x - st.x;
    int nex = en.x > st.x ? 1 : -1;
    int dx = en.x - st.x, dy = en.y - st.y;
    for (int i = 1; i <= n; i++)
    {
        
    }

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, n * sizeof(point), &s[1], GL_STATIC_DRAW);
    glPointSize(8.0f);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(point), (void*)0);
    glEnableVertexAttribArray(0);


}