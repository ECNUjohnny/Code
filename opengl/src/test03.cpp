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

int n, op, u = 8, d = 4, l = 1, r = 2;
unsigned int VAO, VBO;
unsigned int borderVAO, borderVBO;
char s[N];
char *edge = "D:/Code/opengl/data/data.txt", *polygon = "D:/Code/opengl/data/data1.txt";
float xmax = 390, xmin = -390, ymax = 390, ymin = -390, eps = 1e-9;
int tot;
struct vertex
{
    float x, y;
} v[N], w[N];

glm::mat4 Projection = glm::ortho(-450.0f, 450.0f, -450.0f, 450.0f);

const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec2 aPos;\n"
    "uniform mat4 Projection;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = Projection * vec4(aPos, 0.0, 1.0);\n"
    "}\n";

const char *fragmentShaderSource = "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main()\n"
    "{\n"
    "   FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);\n"
    "}\n";

int code(vertex &v)
{
    int code = 0;
    if (v.x < xmin) code |= l;
    if (v.x > xmax) code |= r;
    if (v.y < ymin) code |= d;
    if (v.y > ymax) code |= u;

    return code;
}

int clip_edge(vertex &beg, vertex &en)
{   
    int code1 = code(beg), code2 = code(en);

    while (1)
    {
        if (!(code1 | code2))
        {
            return 1;
        }

        if (code1 & code2)
        {
            return 0;
        }

        vertex &t = code1 ? beg : en;
        int codeout = code1 ? code1 : code2;
        float k = fabs(en.x - beg.x) < eps ? 2e15 : (en.y - beg.y) / (en.x - beg.x);

        if (codeout & u)
        {
            t.x = t.x + (ymax - t.y) / k;
            t.y = ymax;
        }
        else if (codeout & d)
        {
            t.x = t.x + (ymin - t.y) / k;
            t.y = ymin;
        }
        else if (codeout & r)
        {
            t.y = t.y + k * (xmax - t.x);
            t.x = xmax;
        }
        else if (codeout & l)
        {
            t.y = t.y + k * (xmin - t.x);
            t.x = xmin;
        }

        if (codeout == code1) code1 = code(t);
        else code2 = code(t);
    }

    return 1;
}

inline void process_edge(char *loc)
{
    FILE *dat = fopen(loc, "r");
    op = 1;
    if (!dat)
    {
        puts("-1");
        return;
    }

    fscanf(dat, "%d", &n);
    for (int i = 1; i <= n; i++) fscanf(dat, "%f%f", &v[i].x, &v[i].y);
    fclose(dat);

    //for (int i = 1; i <= n; i++) printf("%f %f\n", v[i].x, v[i].y);

    if (!clip_edge(v[1], v[2])) op = 0;

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, n * sizeof(vertex), &v[1], GL_STATIC_DRAW);
}

inline int inside(vertex &v, int bound)
{
    if (bound == 1) return v.x >= xmin;
    else if (bound == 2) return v.y <= ymax;
    else if (bound == 3) return v.x <= xmax;
    else return v.y >= ymin;
}

vertex intersect(vertex &a, vertex &b, int bound, float p)
{
    float k = fabs(a.x - b.x) < eps ? 2e15 : (a.y - b.y) / (a.x - b.x);
    vertex ret;

    if (bound & 1)
    {
        ret.y = k * (p - b.x) + b.y;
        ret.x = p;
    }
    else
    {
        ret.x = (p - b.y) / k + b.x;
        ret.y = p;
    }

    return ret;
}

void process_seg(int bound)
{
    tot = 0;
    
    for (int i = 1; i <= n; i++)
    {
        vertex a = v[i], b = v[i % n + 1];
    
        int c1 = inside(a, bound), c2 = inside(b, bound);

        if (!c1 && !c2) continue;
        else if (c1 && c2)
        {
            w[++tot] = b;
        }
        else if (!c1 && c2)
        {
            if (bound == 1) w[++tot] = intersect(a, b, bound, xmin);
            else if (bound == 2) w[++tot] = intersect(a, b, bound, ymax);
            else if (bound == 3) w[++tot] = intersect(a, b, bound, xmax);
            else w[++tot] = intersect(a, b, bound, ymin);

            w[++tot] = b;
        }
        else
        {
            if (bound == 1) w[++tot] = intersect(a, b, bound, xmin);
            else if (bound == 2) w[++tot] = intersect(a, b, bound, ymax);
            else if (bound == 3) w[++tot] = intersect(a, b, bound, xmax);
            else w[++tot] = intersect(a, b, bound, ymin);
        }
    }

    memcpy(v, w, sizeof(w));
    n = tot;
}

inline void process_polygon(char *loc)
{
    FILE *dat = fopen(loc, "r");
    op = 2;
    if (!dat)
    {
        puts("-1");
        return;
    }

    fscanf(dat, "%d", &n);
    tot = n;
    for (int i = 1; i <= n; i++) fscanf(dat, "%f%f", &v[i].x, &v[i].y);
    fclose(dat);

    //for (int i = 1; i <= n; i++) printf("%f %f\n", v[i].x, v[i].y);

    process_seg(1);
    process_seg(2);
    process_seg(3);
    process_seg(4);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, n * sizeof(vertex), &v[1], GL_STATIC_DRAW);
}

void CharacterCallBack(GLFWwindow* window, unsigned int codepoint)
{
    switch(codepoint)
    {
        case 'e':
            process_edge(edge);
            break;

        case 'p':
            process_polygon(polygon);
            break;

        default:
            break;
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

    int vertexProjectLocation = glGetUniformLocation(shaderProgram, "Projection");
    glUseProgram(shaderProgram);
    glUniformMatrix4fv(vertexProjectLocation, 1, GL_FALSE, glm::value_ptr(Projection));

    glPointSize(7.0f);
    glLineWidth(4.0f);

    while (!glfwWindowShouldClose(window)) 
    {
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);

        glBindVertexArray(borderVAO);
        glDrawArrays(GL_LINE_LOOP, 0, 4);

        glBindVertexArray(VAO);
        if (op == 1) glDrawArrays(GL_LINES, 0, n);
        else if (op == 2) glDrawArrays(GL_LINE_LOOP, 0, n);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    glfwTerminate();
    return 0;
}