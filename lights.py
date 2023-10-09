from math import acos, asin, sqrt
import mt
# Funciones de operación con vectores
def dot(v1, v2):
    return sum(a*b for a, b in zip(v1, v2))

def subtract(v1, v2):
    return [a-b for a, b in zip(v1, v2)]

def multiply_scalar(scalar, v):
    return [scalar * i for i in v]

def norm(v):
    return sqrt(sum(i**2 for i in v))

def normalize(v):
    magnitude = norm(v)
    return [i/magnitude for i in v]

def reflectVector(normal, direction):
    reflect = multiply_scalar(2 * dot(normal, direction), normal)
    reflect = subtract(reflect, direction)
    reflect = normalize(reflect)
    return reflect

def refractVector(normal, incident, n1, n2):
    c1 = dot(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        normal = [-i for i in normal]
        n1, n2 = n2, n1

    n = n1 / n2
    T = [n * incident[i] + n * c1 * normal[i] - normal[i] * (1 - n**2 * (1 - c1**2))**0.5 for i in range(3)]
    T = normalize(T)
    return T

def totalInternalReflection(normal, incident, n1, n2):
    c1 = dot(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    return acos(c1) >= asin(n2 / n1)

def fresnel(normal, incident, n1, n2):
    c1 = dot(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    s2 = (n1 * (1 - c1**2)**0.5) / n2
    c2 = (1 - s2**2)**0.5

    F1 = ((n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2))**2
    F2 = ((n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1))**2

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt
   # Kr = ((n1**0.5-n2**0.5)**2/((n1**0.5+n2**0.5)))    

class Light(object):
    def __init__(self,intensity=1,color=(1,1,1),lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
        
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self,intercept):
        return None
    
    def getSpecularColor(self,intercept,viewPos):
        return None
    
class AmbientLight(Light):
    def __init__(self,intensity=1,color=(1,1,1)):
        super().__init__(intensity,color,"Ambient")
        
class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0),intensity=1, color=(1, 1, 1)):
        self.direction=mt.normalizar_vector(direction)
        super().__init__(intensity, color,"Directional")
        
    def getDiffuseColor(self,intercept):
        dir = [(i*-1) for i in self.direction]
        
        intensity = mt.producto_punto(intercept.normal,dir)*self.intensity
        intensity = max(0,min(1,intensity))
        intensity *= 1-intercept.obj.material.Ks
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [(i*-1) for i in self.direction]
        
        reflect = reflectVector(intercept.normal,dir)
        
        viewDir = mt.subtract_arrays(viewPos,intercept.point)
        viewDir = mt.normalizar_vector(viewDir)
        
        specIntensity = max(0,mt.producto_punto(viewDir,reflect))**intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor
    
class PointLight(Light):
    def __init__(self, point=(0,0,0),intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = mt.subtract_arrays(self.point,intercept.point)
        R = mt.calcular_norma(dir)
        dir = mt.divide_array_scalar(dir,R)
        
        intensity = mt.producto_punto(intercept.normal,dir)*self.intensity
        intensity *= 1-intercept.obj.material.Ks
        
        if R!=0:
            intensity /= R**2
        
        intensity = max(0,min(1,intensity))

        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = mt.subtract_arrays(self.point,intercept.point)
        R = mt.calcular_norma(dir)
        dir = mt.divide_array_scalar(dir,R)
        
        reflect = reflectVector(intercept.normal,dir)
        
        viewDir = mt.subtract_arrays(viewPos,intercept.point)
        viewDir = mt.normalizar_vector(viewDir)
        
        specIntensity = max(0,mt.producto_punto(viewDir,reflect))**intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
        
        specIntensity = max(0,min(1,specIntensity))
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor