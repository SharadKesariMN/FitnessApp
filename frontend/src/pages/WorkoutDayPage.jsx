import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import axios from 'axios';
import { toast } from 'sonner';
import { Activity, ArrowLeft, CheckCircle, Clock, Play } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const WorkoutDayPage = () => {
  const { dayNumber } = useParams();
  const navigate = useNavigate();
  const [dayData, setDayData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedExercise, setSelectedExercise] = useState(null);

  useEffect(() => {
    fetchDayWorkout();
  }, [dayNumber]);

  const fetchDayWorkout = async () => {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/workout/day/${dayNumber}`,
        { withCredentials: true }
      );
      setDayData(response.data);
      if (response.data.exercises.length > 0) {
        setSelectedExercise(response.data.exercises[0]);
      }
    } catch (error) {
      toast.error('Failed to load workout');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteDay = async () => {
    try {
      await axios.post(
        `${BACKEND_URL}/api/workout/complete-day?day_number=${dayNumber}`,
        {},
        { withCredentials: true }
      );
      toast.success('Day completed! Great work!');
      navigate('/dashboard');
    } catch (error) {
      toast.error('Failed to mark as complete');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-volt-blue"></div>
      </div>
    );
  }

  if (!dayData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Workout not found</p>
      </div>
    );
  }

  const totalDuration = dayData.exercises.reduce((sum, ex) => sum + ex.duration_minutes, 0);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="glass border-b border-border sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Button
            data-testid="back-btn"
            variant="ghost"
            onClick={() => navigate('/dashboard')}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Dashboard
          </Button>
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-volt-blue" />
            <h1 className="text-2xl font-heading font-black tracking-tight">Day {dayNumber}</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Exercise List */}
          <div className="lg:col-span-1">
            <Card data-testid="exercise-list-card" className="border-border sticky top-24">
              <CardHeader>
                <CardTitle className="font-heading">Today's Exercises</CardTitle>
                <CardDescription>
                  {dayData.exercises.length} exercises • ~{totalDuration} min
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {dayData.exercises.map((exercise, index) => (
                  <div
                    key={exercise.exercise_id}
                    data-testid={`exercise-item-${index}`}
                    onClick={() => setSelectedExercise(exercise)}
                    className={`p-4 rounded-lg cursor-pointer transition-all ${
                      selectedExercise?.exercise_id === exercise.exercise_id
                        ? 'bg-volt-blue/20 border-2 border-volt-blue'
                        : 'bg-secondary hover:bg-secondary/80 border-2 border-transparent'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-medium text-sm">{exercise.name}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <Clock className="w-3 h-3 text-muted-foreground" />
                          <span className="text-xs text-muted-foreground">
                            {exercise.duration_minutes} min
                          </span>
                          <Badge variant="outline" className="text-xs">
                            {exercise.difficulty}
                          </Badge>
                        </div>
                      </div>
                      <Play className="w-4 h-4 text-volt-blue" />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Exercise Detail */}
          <div className="lg:col-span-2">
            {selectedExercise && (
              <motion.div
                key={selectedExercise.exercise_id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card data-testid="exercise-detail-card" className="border-border mb-6">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="font-heading text-2xl mb-2">
                          {selectedExercise.name}
                        </CardTitle>
                        <CardDescription className="text-base">
                          {selectedExercise.description}
                        </CardDescription>
                      </div>
                      <Badge className="bg-volt-blue text-white">
                        {selectedExercise.sport_category}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Exercise Demo */}
                    <div className="exercise-demo">
                      <img
                        src={selectedExercise.gif_url}
                        alt={selectedExercise.name}
                        className="w-full h-full object-cover"
                        data-testid="exercise-gif"
                      />
                    </div>

                    {/* Instructions */}
                    <div>
                      <h3 className="font-heading font-bold text-lg mb-3">Instructions</h3>
                      <ol className="space-y-2">
                        {selectedExercise.instructions.map((instruction, index) => (
                          <li
                            key={index}
                            className="flex gap-3 text-muted-foreground"
                            data-testid={`instruction-${index}`}
                          >
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-volt-blue/20 text-volt-blue flex items-center justify-center text-sm font-bold">
                              {index + 1}
                            </span>
                            <span>{instruction}</span>
                          </li>
                        ))}
                      </ol>
                    </div>

                    {/* Duration Info */}
                    <div className="p-4 bg-secondary rounded-lg">
                      <div className="flex items-center gap-2">
                        <Clock className="w-5 h-5 text-volt-blue" />
                        <span className="font-medium">Duration:</span>
                        <span className="text-muted-foreground">
                          {selectedExercise.duration_minutes} minutes
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Complete Day Button */}
                <Card data-testid="complete-day-card" className="border-volt-blue/50 bg-volt-blue/5">
                  <CardContent className="pt-6">
                    <div className="text-center">
                      <h3 className="font-heading font-bold text-xl mb-2">
                        {dayData.completed ? 'Day Completed!' : 'Finish Your Workout'}
                      </h3>
                      <p className="text-muted-foreground mb-4">
                        {dayData.completed
                          ? 'Great job! You can review exercises anytime.'
                          : 'Mark this day as complete once you finish all exercises'}
                      </p>
                      {!dayData.completed && (
                        <Button
                          data-testid="mark-complete-btn"
                          onClick={handleCompleteDay}
                          size="lg"
                          className="btn-hover bg-volt-blue hover:bg-volt-blue/90 font-bold"
                        >
                          <CheckCircle className="w-5 h-5 mr-2" />
                          Mark Day as Complete
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default WorkoutDayPage;
