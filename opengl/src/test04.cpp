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
char *vertShader, *fragShader, ch;
mat4 Projection = glm::ortho(-25.0f, 25.0f, -25.0f, 25.0f);

struct point
{
    float x, y;
} s[N], st, en;

int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    //puts("1");

    GLFWwindow *window = glfwCreateWindow(1200, 1200, "Breshham", nullptr, nullptr);
    glfwMakeContextCurrent(window);
    //puts("1");

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);
    //puts("1");

    FILE *file = fopen("D:/Code/opengl/data/data.txt", "r");
    fscanf(file, "%f%f%f%f", &st.x, &st.y, &en.x, &en.y);
    fclose(file);
    //puts("1");

    n = en.x - st.x;
    int dx = en.x - st.x, dy = en.y - st.y, p = 2 * dy - dx;
    float x = st.x, y = st.y;
    for (int i = 1; i <= n; i++)
    {
        s[i] = {x, y};
        if (p >= 0) y += 1, p += 2 * (dy - dx);
        else p += 2 * dy;
        x += 1;
    }
    //puts("1");

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, n * sizeof(point), &s[1], GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(point), (void*)0);
    glEnableVertexAttribArray(0);
    //puts("1");

    vertShader = new char[N];
    fragShader = new char[N];
    //puts("1");

    file = fopen("D:/Code/opengl/src/vert.glsl", "r");
    while (~(ch = fgetc(file))) vertShader[m++] = ch;
    vertShader[m] = 0;
    fclose(file);
    puts(vertShader);

    m = 0;
    file = fopen("D:/Code/opengl/src/frag.glsl", "r");
    while (~(ch = fgetc(file))) fragShader[m++] = ch;
    fragShader[m] = 0;
    fclose(file);
    //puts("fragShader");

    vert = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vert, 1, &vertShader, NULL);
    glCompileShader(vert);

    frag = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(frag, 1, &fragShader, NULL);
    glCompileShader(frag);

    shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vert);
    glAttachShader(shaderProgram, frag);
    glLinkProgram(shaderProgram);

    glDeleteShader(frag);
    glDeleteShader(vert);
    //puts("1");

    int projection = glGetUniformLocation(shaderProgram, "Projection");
    glUseProgram(shaderProgram);
    glUniformMatrix4fv(projection, 1, GL_FALSE, glm::value_ptr(Projection));

    glPointSize(3.0f);

    while (!glfwWindowShouldClose(window))
    {
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);

        glBindVertexArray(VAO);
        glDrawArrays(GL_POINTS, 0, n);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    glfwTerminate();

    return 0;
}