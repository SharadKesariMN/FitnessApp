import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import axios from 'axios';
import { toast } from 'sonner';
import { Activity, ArrowLeft, Users, Dumbbell, Trash2 } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const AdminPage = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleteTarget, setDeleteTarget] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersRes, exercisesRes] = await Promise.all([
        axios.get(`${BACKEND_URL}/api/admin/users`, { withCredentials: true }),
        axios.get(`${BACKEND_URL}/api/admin/exercises`, { withCredentials: true }),
      ]);
      setUsers(usersRes.data);
      setExercises(exercisesRes.data);
    } catch (error) {
      toast.error('Failed to load admin data');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`${BACKEND_URL}/api/admin/users/${userId}`, {
        withCredentials: true,
      });
      toast.success('User deleted');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete user');
    }
    setDeleteTarget(null);
  };

  const handleDeleteExercise = async (exerciseId) => {
    try {
      await axios.delete(`${BACKEND_URL}/api/admin/exercises/${exerciseId}`, {
        withCredentials: true,
      });
      toast.success('Exercise deleted');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete exercise');
    }
    setDeleteTarget(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-volt-blue"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="glass border-b border-border sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Button
            data-testid="back-to-dashboard-btn"
            variant="ghost"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-volt-blue" />
            <h1 className="text-2xl font-heading font-black tracking-tight">Admin Panel</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <Tabs defaultValue="users" className="space-y-6">
          <TabsList data-testid="admin-tabs" className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger data-testid="users-tab" value="users" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Users ({users.length})
            </TabsTrigger>
            <TabsTrigger data-testid="exercises-tab" value="exercises" className="flex items-center gap-2">
              <Dumbbell className="w-4 h-4" />
              Exercises ({exercises.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="users">
            <Card data-testid="users-card" className="border-border">
              <CardHeader>
                <CardTitle className="font-heading">User Management</CardTitle>
                <CardDescription>View and manage all registered users</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Goal</TableHead>
                        <TableHead>Sport</TableHead>
                        <TableHead>BMI</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {users.map((user) => (
                        <TableRow key={user.user_id} data-testid={`user-row-${user.user_id}`}>
                          <TableCell className="font-medium">{user.name}</TableCell>
                          <TableCell>{user.email}</TableCell>
                          <TableCell>{user.fitness_goal || '-'}</TableCell>
                          <TableCell>{user.selected_sport || '-'}</TableCell>
                          <TableCell>{user.bmi || '-'}</TableCell>
                          <TableCell>
                            {user.is_guest ? 'Guest' : 'Registered'}
                            {user.is_admin && ' (Admin)'}
                          </TableCell>
                          <TableCell className="text-right">
                            <Button
                              data-testid={`delete-user-btn-${user.user_id}`}
                              variant="ghost"
                              size="sm"
                              onClick={() => setDeleteTarget({ type: 'user', id: user.user_id, name: user.name })}
                            >
                              <Trash2 className="w-4 h-4 text-electric-blaze" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="exercises">
            <Card data-testid="exercises-card" className="border-border">
              <CardHeader>
                <CardTitle className="font-heading">Exercise Management</CardTitle>
                <CardDescription>View and manage workout exercises</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Category</TableHead>
                        <TableHead>Duration</TableHead>
                        <TableHead>Difficulty</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {exercises.map((exercise) => (
                        <TableRow key={exercise.exercise_id} data-testid={`exercise-row-${exercise.exercise_id}`}>
                          <TableCell className="font-medium">{exercise.name}</TableCell>
                          <TableCell>{exercise.sport_category}</TableCell>
                          <TableCell>{exercise.duration_minutes} min</TableCell>
                          <TableCell>{exercise.difficulty}</TableCell>
                          <TableCell className="text-right">
                            <Button
                              data-testid={`delete-exercise-btn-${exercise.exercise_id}`}
                              variant="ghost"
                              size="sm"
                              onClick={() =>
                                setDeleteTarget({ type: 'exercise', id: exercise.exercise_id, name: exercise.name })
                              }
                            >
                              <Trash2 className="w-4 h-4 text-electric-blaze" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete {deleteTarget?.name}. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              data-testid="confirm-delete-btn"
              onClick={() => {
                if (deleteTarget?.type === 'user') {
                  handleDeleteUser(deleteTarget.id);
                } else if (deleteTarget?.type === 'exercise') {
                  handleDeleteExercise(deleteTarget.id);
                }
              }}
              className="bg-electric-blaze hover:bg-electric-blaze/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default AdminPage;
