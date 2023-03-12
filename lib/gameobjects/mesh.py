#!/usr/bin/env python


class Mesh(object):
    
    def __init__(self):
        
        self.vertices = []
        self.texture_coords = []
        self.vertex_normals = []
        
        self.faces = []
        
    def read_obj(self, file_in):
        
        for line in file_in:
            words = line.split()
            
            if not words:
                continue
            
            data_type = words[0]
            data = words[1:]
            
            if date_type == '#': # Comment
                continue
            
            if data_type == 'v': # Vertex
                # v x y z
                vertex = float(data[0]), float(data[1]), float(data[2])
                self.vertices.append(vertex)
            
            elif data_type == 'vt': # Texture coordinate
                #vt u v
                texture_coord = float(data[0]), float(data[1])
                self.vertices.append(texture_coord)
            
            elif data_type == 'vn': # Vertex normal
                #vn x y z
                normal = float(data[0]), float(data[1]), float(data[2])
                self.vertex_normals.append(normal)
            
            elif data_type == 'f': # Face
                #f vertex_index, texture_index, normal_index
                for word in data:
                    triplet = word.split('/')
                    face = int(triplet[0]), int(triplet[1]), int(triplet[2])
                    self.faces.append(face)
    
    def draw(self):
        
        glBegin(GL_TRIS)
        
        for vertex_index, texture_index, normal_index in self.faces:
            
            glTexCoord(self.texture_coords[texture_index])
            glNormal(self.normals[normal_index])
            glVertex(vertices[vertex_index])
            
        glEnd()
        
if __name__ == "__main__":
    
    mesh = Mesh()
    mesh.read_obj(file("will31.obj"))
    print mesh.vertices