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

ifstream vertFile, fragFile;
stringstream vertString, fragString;
const char *vertCode, *fragCode;
string tmp_vert, tmp_frag;

float cube[] = 
{
    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f,  
     1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f,  1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f,  1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f,  1.0f, -1.0f,  0.0f, 1.0f, 0.0f,  
    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f,  

    -1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f,  
     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f,  
    -1.0f,  1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,

    -1.0f,  1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f,  1.0f, -1.0f,  0.0f, 1.0f, 0.0f, 
    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f, 
    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f, 
    -1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f,  1.0f,  1.0f,  0.0f, 0.0f, 0.0f,

     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f, 
     1.0f,  1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f, 

    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f, 
     1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
     1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f, -1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f, -1.0f, -1.0f,  0.0f, 0.0f, 1.0f, 

    -1.0f,  1.0f, -1.0f,  0.0f, 1.0f, 0.0f, 
     1.0f,  1.0f, -1.0f,  0.0f, 0.0f, 0.0f,
     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f, 
     1.0f,  1.0f,  1.0f,  1.0f, 0.0f, 0.0f, 
    -1.0f,  1.0f,  1.0f,  0.0f, 0.0f, 0.0f,
    -1.0f,  1.0f, -1.0f,  0.0f, 1.0f, 0.0f  
};

int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    
    GLFWwindow* window = glfwCreateWindow(1200, 1200, "Color", nullptr, nullptr);
    glfwMakeContextCurrent(window);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    glEnable(GL_DEPTH_TEST);

    unsigned int VAO, VBO;
    glGenBuffers(1, &VBO);
    glGenVertexArrays(1, &VAO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(cube), cube, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 6, (void*)0);
    glEnableVertexAttribArray(0);

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 6, (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    vertFile.open("D:/Code/opengl/src/vert.glsl");
    fragFile.open("D:/Code/opengl/src/frag.glsl");

    vertString << vertFile.rdbuf();
    fragString << fragFile.rdbuf();

    tmp_vert = vertString.str();
    tmp_frag = fragString.str();

    vertCode = tmp_vert.c_str();
    fragCode = tmp_frag.c_str();

    unsigned int vert = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vert, 1, &vertCode, NULL);
    glCompileShader(vert);

    unsigned int frag = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(frag, 1, &fragCode, NULL);
    glCompileShader(frag);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vert); 
    glAttachShader(shaderProgram, frag);
    glLinkProgram(shaderProgram);

    int modelLoc = glGetUniformLocation(shaderProgram, "Model");
    int viewLoc = glGetUniformLocation(shaderProgram, "View");
    int projectionLoc = glGetUniformLocation(shaderProgram, "Projection");

    glDeleteShader(frag);
    glDeleteShader(vert);

    while (!glfwWindowShouldClose(window))
    {
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(shaderProgram);

        mat4 Model = glm::rotate(mat4(1.0f), (float)glfwGetTime(), vec3(0.5f, 1.0f, 0.0f));
        mat4 Projection = glm::perspective(glm::radians(45.0f), (float)(1200) / (float)1200, 0.1f, 100.0f);
        mat4 View = glm::translate(mat4(1.0f), vec3(0.0f, 0.0f, -6.0f));

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, value_ptr(Model));
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, value_ptr(View));
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, value_ptr(Projection));

        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 36);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwTerminate();

    return 0;
}